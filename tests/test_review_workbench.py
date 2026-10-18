"""SYNTHETIC actors/events/authorities only. No real legal approval is asserted."""

import base64
from copy import deepcopy
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import review_workbench as w


class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for p in ('schemas/review-record.schema.json', 'data/reviews/templates/common-v1.json'):
            target = self.root / p
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(w.ROOT / p, target)
        self.manifest = {'revision': 'a'*40, 'files': [
            {'path': 'SKILL.md', 'blob_sha': 'b'*40, 'decision': 'eligible-for-scope-review'},
            {'path': 'excluded.md', 'blob_sha': 'c'*40, 'decision': 'exclude-from-hosting'}]}
        self.subject = {'subject_id': 'synthetic-new-legal-skill', 'subject_type': 'skill',
                        'source_url': 'https://github.com/example/synthetic/blob/'+'a'*40+'/SKILL.md',
                        'source_revision': 'a'*40, 'scope_manifest_ref': 'data/test-inventory-v1.json',
                        'templates': ['data/reviews/templates/common-v1.json'], 'jurisdiction': 'CN-Mainland',
                        'track': 'curated-hosting', 'review_scope': ['SKILL.md'], 'excluded_scope': ['excluded.md'],
                        'public_summary_only': True}
        w.write(self.root / self.subject['scope_manifest_ref'], self.manifest)
        self.subject_ref = 'data/synthetic-subject.json'
        w.write(self.root / self.subject_ref, self.subject)
        self.rid = w.init_review(self.root, self.subject_ref, rid='RV-synthetic-one')
        self.directory = w.case_dir(self.root, self.rid)
        self.events, self.actor_type, self.roles = {}, 'User', list(w.ROLES.values())
        self.permission, self.head, self.base = 'admin', 'd'*40, 'e'*40

    def record(self):
        return w.load_case(self.root, self.rid)

    def form(self, complete=False, changes=None):
        path = self.directory / 'workbook.md'
        sections = w.parse_workbook(path.read_text())
        sections['signature'] = {'credential_evidence_ref': 'controlled://synthetic/credential',
                                 'conflict_declaration': 'SYNTHETIC no conflict fixture', 'regulatory_as_of': w.now()[:10]}
        sections['maintenance'] = {'next_review_date': '2099-01-01', 'risk_level': 'low'}
        if complete:
            for c in self.record()['checks']:
                values = sections[c['check_id']]
                for key in w.CHECK_FIELDS:
                    if key in ('authority_refs', 'evidence_refs'):
                        values[key] = 'https://example.invalid/synthetic-authority'
                    elif key == 'check_status':
                        values[key] = 'pass'
                    elif key == 'risk_level':
                        values[key] = 'low'
                    elif key == 'required_changes':
                        values[key] = ''
                    else:
                        values[key] = 'SYNTHETIC applicable reasoning, not legal advice'
            for axis in ('rights_review', 'engineering_review', 'admission_decision'):
                for key in sections[axis]:
                    sections[axis][key] = 'https://example.invalid/synthetic-gate'
        for section, fields in (changes or {}).items():
            sections[section].update(fields)
        content = '# SYNTHETIC test fixture only\n\n'
        for name, values in sections.items():
            content += '## '+name+'\n'+'\n'.join(f'- {k}: {v}' for k, v in values.items())+'\n\n'
        w.write(path, content)
        return content

    def start(self):
        w.start(self.root, self.rid, 'synthetic-human', 'SYNTHETIC submit', 'https://example.invalid/submission')

    def event(self, axis, decision, binding=None):
        eid = len(self.events)+100
        url = f'https://github.com/fitalex/LexRouter/pull/999#pullrequestreview-{eid}'
        digest = binding or w.binding(self.record(), (self.directory / 'workbook.md').read_text())
        self.events[str(eid)] = {'id': eid, 'html_url': url, 'state': 'COMMENTED', 'submitted_at': w.now(),
                                'user': {'login': 'synthetic-human', 'type': self.actor_type}, 'commit_id': self.head,
                                'body': f'LexRouter-Review: {self.rid}\nRole: {axis}\nDecision: {decision}\nBinding-SHA256: {digest}\nPolicy-Base: {self.base}\nReason: SYNTHETIC test decision'}
        return url

    def api(self, path):
        if '/pulls/' in path and '/reviews/' in path:
            return deepcopy(self.events[path.rsplit('/', 1)[-1]])
        if '/pulls/' in path:
            return {'head': {'sha': self.head}, 'base': {'sha': self.base, 'ref': 'main', 'repo': {'full_name': 'fitalex/LexRouter'}}}
        if '/contents/' in path:
            self.assertTrue(path.endswith('?ref='+self.base))
            policy = {'repository': 'fitalex/LexRouter', 'reviewers': {'synthetic-human': self.roles}}
            return {'content': base64.b64encode(json.dumps(policy).encode()).decode()}
        if '/collaborators/' in path:
            return {'permission': self.permission}
        if '/compare/' in path:
            return {'status': 'ahead'}
        self.fail('Unexpected evidence API call')

    def sync(self, axis, decision):
        url = self.event(axis, decision)
        w.sync_event(self.root, self.rid, url, self.api)
        return url

    def approve_professional(self):
        self.start()
        self.form(complete=True)
        return self.sync('professional_review', 'approved-scope')

    def child(self, trigger, revision='f'*40, scope=None):
        subject, manifest = deepcopy(self.subject), deepcopy(self.manifest)
        subject['source_revision'] = manifest['revision'] = revision
        subject['scope_manifest_ref'] = 'data/test-inventory-v2.json'
        manifest['files'][0]['blob_sha'] = '1'*40
        if scope:
            subject['review_scope'] = scope
            manifest['files'].append({'path': 'new.md', 'blob_sha': '2'*40, 'decision': 'eligible-for-scope-review'})
        w.write(self.root / subject['scope_manifest_ref'], manifest)
        w.write(self.root / 'data/next-subject.json', subject)
        return w.init_review(self.root, 'data/next-subject.json', trigger, self.rid, 'RV-synthetic-two')

    def test_T01_arbitrary_new_skill_without_core_code(self):
        r = self.record()
        self.assertEqual(r['subject_id'], 'synthetic-new-legal-skill')
        self.assertEqual(len(r['checks']), 10)
        self.assertEqual(r['professional_review']['status'], 'pending')
        self.assertIsNone(r['professional_review']['signature'])
        self.assertEqual(w.validate_record(self.root, r), [])
        for name in ('packet.md', 'matrix.md', 'evidence.md', 'workbook.md'):
            self.assertTrue((self.directory / name).is_file())

    def test_T02_new_version_preserves_signed_history(self):
        self.approve_professional()
        self.sync('rights_review', 'approved-scope')
        self.sync('engineering_review', 'passed')
        self.sync('admission_decision', 'admitted')
        w.archive(self.root, self.rid)
        before = {p.name: p.read_bytes() for p in self.directory.glob('*.json')}
        child = w.load_case(self.root, self.child('source-update'))
        self.assertEqual(child['parent_review_id'], self.rid)
        self.assertEqual(child['status'], 'evidence-ready')
        self.assertTrue(all(c['check_status'] == 'pending' for c in child['checks']))
        self.assertEqual(w.validate_record(self.root, self.record(), True, self.api), [])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.directory.glob('*.json')})

    def test_T03_regulatory_change_lists_affected_checks(self):
        rid = self.child('regulatory-change', revision='a'*40)
        result = w.diff_reviews(self.root, self.rid, rid, '官方')
        self.assertIn('C03', result['checks_requiring_confirmation'])
        self.assertEqual(result['confirmation_status'], 'pending-professional-confirmation')
        self.assertIsNone(w.load_case(self.root, rid)['professional_review']['signature'])

    def test_T04_major_errors_and_missing_authority_block_approval(self):
        self.start()
        self.form(complete=True, changes={'C05': {'check_status': 'fail', 'required_changes': 'SYNTHETIC major error'}})
        with self.assertRaises(w.ReviewError):
            self.sync('professional_review', 'approved-scope')
        self.assertEqual(self.record()['status'], 'in-review')
        self.form(complete=True, changes={'C05': {'authority_refs': ''}})
        with self.assertRaises(w.ReviewError):
            self.sync('professional_review', 'approved-scope')

    def test_T05_rights_pending_blocks_admission(self):
        self.approve_professional()
        self.assertFalse(w.admission_ready(self.record()))
        with self.assertRaises(w.ReviewError):
            self.sync('admission_decision', 'admitted')
        self.assertEqual(self.record()['admission_decision']['status'], 'not-admitted')

    def test_T06_prepare_preserves_human_opinion_and_no_signature(self):
        content = self.form(changes={'C05': {'finding': 'SYNTHETIC draft multiline\nsecond line'}})
        for _ in range(3):
            w.prepare(self.root, self.rid)
        self.assertEqual((self.directory / 'workbook.md').read_text(), content)
        self.assertIsNone(self.record()['professional_review']['signature'])
        (self.directory / 'matrix.md').write_text('Human modified generated material')
        with self.assertRaisesRegex(w.ReviewError, 'conflict'):
            w.prepare(self.root, self.rid)
        self.assertEqual((self.directory / 'workbook.md').read_text(), content)

    def test_T07_expanded_scope_has_no_inherited_approval(self):
        self.approve_professional()
        rid = self.child('scope-change', scope=['SKILL.md', 'new.md'])
        child = w.load_case(self.root, rid)
        self.assertIsNone(child['professional_review']['signature'])
        self.assertEqual(w.diff_reviews(self.root, self.rid, rid)['added_scope'], ['new.md'])
        child['review_scope'].append('excluded.md')
        self.assertTrue(w.validate_record(self.root, child))

    def test_T08_privacy_no_private_import_or_log_echo(self):
        marker = 'PRIVATE_MATERIAL_SYNTHETIC_DO_NOT_LOG'
        (self.directory / 'workbook.md').write_text(marker)
        stream = io.StringIO()
        with redirect_stderr(stream):
            result = w.main(['--root', str(self.root), 'validate'])
        self.assertEqual(result, 1)
        self.assertNotIn(marker, stream.getvalue())
        for ref in ('file:///private/synthetic', 'https://example.invalid/evidence?token=synthetic'):
            with self.assertRaises(w.ReviewError):
                w.reference(ref)
        with self.assertRaises(w.ReviewError):
            w.safe(self.root, '../escape')
        (self.root / 'linked').symlink_to('/tmp')
        with self.assertRaises(w.ReviewError):
            w.safe(self.root, 'linked/private')

    def test_full_human_cycle_independent_dimensions_archive_online(self):
        url = self.approve_professional()
        self.assertFalse(w.sync_event(self.root, self.rid, url, self.api))
        self.sync('rights_review', 'approved-scope')
        self.sync('engineering_review', 'passed')
        self.assertTrue(w.admission_ready(self.record()))
        self.sync('admission_decision', 'admitted')
        r = self.record()
        self.assertEqual(len({r[x]['signature']['signature_evidence_ref'] for x in w.ROLES}), 4)
        self.assertEqual(w.validate_record(self.root, r, True, self.api), [])
        w.archive(self.root, self.rid)
        w.archive(self.root, self.rid)
        self.assertEqual(w.validate_record(self.root, self.record(), True, self.api), [])
        with self.assertRaises(w.ReviewError):
            w.prepare(self.root, self.rid)

    def test_needs_changes_requires_human_resubmission(self):
        self.start()
        self.form(changes={'C04': {'check_status': 'needs-changes', 'finding': 'SYNTHETIC missing time evidence'}})
        self.sync('professional_review', 'needs-changes')
        original = next((self.directory / 'history').glob('*.json')).read_bytes()
        self.form(complete=True)
        with self.assertRaises(w.ReviewError):
            self.sync('professional_review', 'approved-scope')
        self.start()
        self.sync('professional_review', 'approved-scope')
        self.assertEqual(original, sorted((self.directory / 'history').glob('*.json'))[0].read_bytes())
        self.assertEqual(w.validate_record(self.root, self.record(), True, self.api), [])

    def test_signature_requires_user_policy_permission_and_exact_binding(self):
        self.start()
        self.form(complete=True)
        cases = [('Bot', self.roles, 'admin', None), ('User', [], 'admin', None),
                 ('User', self.roles, 'read', None), ('User', self.roles, 'admin', '0'*64)]
        for actor, roles, permission, digest in cases:
            self.actor_type, self.roles, self.permission = actor, roles, permission
            with self.assertRaises(w.ReviewError):
                w.sync_event(self.root, self.rid, self.event('professional_review', 'approved-scope', digest), self.api)
        self.assertIsNone(self.record()['professional_review']['signature'])

    def test_stale_or_dismissed_event_is_rejected(self):
        self.start()
        self.form(complete=True)
        url = self.event('professional_review', 'approved-scope')
        event = self.events[url.rsplit('-', 1)[-1]]
        event['commit_id'] = '0'*40
        with self.assertRaises(w.ReviewError):
            w.sync_event(self.root, self.rid, url, self.api)
        event['commit_id'], event['state'] = self.head, 'DISMISSED'
        with self.assertRaises(w.ReviewError):
            w.sync_event(self.root, self.rid, url, self.api)

    def test_snapshot_tampering_and_forged_plain_json_are_rejected(self):
        self.approve_professional()
        r = self.record()
        r['rights_review']['status'] = 'approved-scope'
        self.assertTrue(w.validate_record(self.root, r))
        path = next((self.directory / 'history').glob('*.json'))
        snap = w.read(path)
        snap['after']['checks'][0]['finding'] = 'SYNTHETIC tampered'
        w.write(path, snap)
        self.assertTrue(w.validate_record(self.root, self.record()))

    def test_signed_legal_fields_frozen_independent_roles_can_fill_forms(self):
        self.approve_professional()
        self.form(changes={'rights_review': {'hosting-scope': 'https://example.invalid/new-rights-evidence'}})
        self.sync('rights_review', 'approved-scope')
        self.assertEqual(w.validate_record(self.root, self.record()), [])
        self.form(changes={'C05': {'finding': 'SYNTHETIC silently altered legal opinion'}})
        self.assertTrue(w.validate_record(self.root, self.record()))

    def test_unique_ids_parent_cycles_and_template_conflicts(self):
        with self.assertRaises(w.ReviewError):
            w.init_review(self.root, self.subject_ref, rid=self.rid)
        with self.assertRaises(w.ReviewError):
            w.init_review(self.root, self.subject_ref)
        r = self.record()
        r['parent_review_id'] = self.rid
        self.assertTrue(w.validate_record(self.root, r))
        custom = w.read(self.root / self.subject['templates'][0])
        custom['template_id'] = 'custom-duplicate-tag'
        w.write(self.root / 'data/custom-template.json', custom)
        checks, _ = w.templates(self.root, self.subject['templates']+['data/custom-template.json'])
        self.assertEqual(len(checks), 10)
        custom['checks'][0]['legal_issue'] = 'SYNTHETIC conflicting rule'
        w.write(self.root / 'data/custom-template.json', custom)
        with self.assertRaises(w.ReviewError):
            w.templates(self.root, self.subject['templates']+['data/custom-template.json'])

    def test_three_real_subjects_create_unsigned_exact_scope(self):
        # Reinitialize fixed input subjects in isolation. Future production reviews,
        # real human decisions and newly added Skills must not break this test.
        expected = {'discovery-contract-review': (27, 15), 'discovery-contract-review-zh': (4, 15), 'discovery-china-legal-counsel': (19, 16)}
        for cid, (count, checks) in expected.items():
            ref = f'data/reviews/subjects/{cid}.json'
            subject = w.read(w.ROOT / ref)
            for rel in [ref, subject['scope_manifest_ref'], *subject['templates']]:
                w.write(self.root / rel, w.read(w.ROOT / rel))
            rid = w.init_review(self.root, ref, rid='RV-'+cid)
            r = w.load_case(self.root, rid)
            self.assertEqual((len(r['review_scope']), len(r['checks'])), (count, checks))
            self.assertEqual(r['status'], 'evidence-ready')
            self.assertEqual(r['jurisdiction']['status'], 'proposed')
            self.assertTrue(all(r[x]['signature'] is None for x in w.ROLES))
            self.assertEqual(w.validate_record(self.root, r), [])

    def test_signed_history_protected_against_git_baseline(self):
        self.approve_professional()
        for args in (['init', '-q'], ['add', '.'], ['-c', 'user.name=Synthetic', '-c', 'user.email=synthetic@example.invalid', 'commit', '-qm', 'synthetic baseline']):
            subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True)
        self.assertEqual(w.immutable_history(self.root, 'HEAD'), [])
        next((self.directory / 'history').glob('*.json')).unlink()
        self.assertTrue(w.immutable_history(self.root, 'HEAD'))

    def test_all_track_specific_rights_gates(self):
        for track in w.GATES:
            with self.subTest(track=track):
                subject = deepcopy(self.subject)
                subject.update(subject_id='synthetic-'+track, track=track)
                w.write(self.root / 'data/track-subject.json', subject)
                self.rid = w.init_review(self.root, 'data/track-subject.json', rid='RV-'+track)
                self.directory = w.case_dir(self.root, self.rid)
                self.form()
                with self.assertRaises(w.ReviewError):
                    self.sync('rights_review', 'approved-scope')
                self.form(complete=True)
                self.sync('rights_review', 'approved-scope')
                self.assertEqual(self.record()['rights_review']['status'], 'approved-scope')
                self.assertEqual(w.validate_record(self.root, self.record(), True, self.api), [])

    def test_suspension_preserves_evidence_and_blocks_admission(self):
        self.approve_professional()
        original = next((self.directory / 'history').glob('*.json')).read_bytes()
        self.form(changes={'suspension': {'affected_scope': 'SKILL.md', 'reason': 'SYNTHETIC credible risk'}})
        self.sync('admission_decision', 'suspended')
        self.assertEqual(self.record()['suspension']['affected_scope'], ['SKILL.md'])
        self.assertFalse(w.admission_ready(self.record()))
        self.assertEqual(w.validate_record(self.root, self.record()), [])
        self.assertEqual(original, sorted((self.directory / 'history').glob('*.json'))[0].read_bytes())

    def test_due_review_todos_and_scheduled_trigger(self):
        self.approve_professional()
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(w.main(['--root', str(self.root), 'status', '--as-of', '2100-01-01']), 0)
        self.assertIn('True', output.getvalue())
        self.assertIn('rights_review', output.getvalue())
        child = w.load_case(self.root, self.child('scheduled-review'))
        self.assertEqual(child['professional_review']['status'], 'pending')
    def test_non_github_source_and_encoded_file_path_without_core_changes(self):
        subject, inventory = deepcopy(self.subject), deepcopy(self.manifest)
        subject.update(subject_id='synthetic-gitlab-source', source_url='https://gitlab.example.invalid/skill',
                       source_file_url_template='https://gitlab.example.invalid/skill/-/blob/{revision}/{path}',
                       scope_manifest_ref='data/gitlab-inventory.json', review_scope=['legal file.md'])
        inventory['files'][0]['path'] = 'legal file.md'
        w.write(self.root / subject['scope_manifest_ref'], inventory)
        w.write(self.root / 'data/gitlab-subject.json', subject)
        rid = w.init_review(self.root, 'data/gitlab-subject.json', rid='RV-gitlab-synthetic')
        evidence = (w.case_dir(self.root, rid) / 'evidence.md').read_text()
        self.assertIn('/blob/'+'a'*40+'/legal%20file.md', evidence)
        self.assertEqual(w.validate_record(self.root, w.load_case(self.root, rid)), [])

    def test_admitted_dimension_cannot_be_silently_downgraded(self):
        self.approve_professional()
        self.sync('rights_review', 'approved-scope')
        self.sync('engineering_review', 'passed')
        self.sync('admission_decision', 'admitted')
        with self.assertRaises(w.ReviewError):
            self.sync('rights_review', 'needs-changes')
        self.assertEqual(w.validate_record(self.root, self.record()), [])
    def test_interrupted_write_and_duplicate_json_keys_fail_closed(self):
        w.write(self.directory / 'history/orphan.json', {'synthetic': True})
        self.assertTrue(w.validate_record(self.root, self.record()))
        (self.directory / 'history/orphan.json').unlink()
        (self.directory / 'record.json').write_text('{"status":"draft","status":"approved-scope"}')
        stream = io.StringIO()
        with redirect_stderr(stream):
            self.assertEqual(w.main(['--root', str(self.root), 'validate']), 1)
        self.assertIn('Duplicate JSON keys', stream.getvalue())
    def test_rejected_signed_opinion_is_also_immutable(self):
        self.start()
        self.form(changes={'C05': {'check_status': 'fail', 'finding': 'SYNTHETIC rejection reason'}})
        self.sync('professional_review', 'rejected')
        self.assertEqual(w.validate_record(self.root, self.record()), [])
        self.form(changes={'C05': {'finding': 'SYNTHETIC overwritten rejection'}})
        self.assertTrue(w.validate_record(self.root, self.record()))
        with self.assertRaises(w.ReviewError):
            w.archive(self.root, self.rid)


if __name__ == '__main__':
    unittest.main()
