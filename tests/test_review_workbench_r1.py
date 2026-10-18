"""LR-P1-02-R1 regressions; all actors, decisions and evidence are SYNTHETIC."""

from pathlib import Path
import unittest
from unittest import mock

import test_review_workbench as fixtures

w = fixtures.w


class ReviewControlTests(unittest.TestCase):
    def new_case(self):
        case = fixtures.WorkbenchTests()
        self.addCleanup(case.doCleanups)
        case.setUp()
        return case

    def setUp(self):
        self.case = self.new_case()

    @staticmethod
    def files(case):
        return {str(p.relative_to(case.directory)): p.read_bytes()
                for p in case.directory.rglob('*') if p.is_file()}

    def assert_archive_refused_unchanged(self, case):
        before = self.files(case)
        with self.assertRaises(w.ReviewError):
            w.archive(case.root, case.rid)
        self.assertEqual(self.files(case), before)

    @staticmethod
    def complete(case, final='admitted'):
        case.approve_professional()
        case.sync('rights_review', 'approved-scope')
        case.sync('engineering_review', 'passed')
        if final == 'suspended':
            case.form(changes={'suspension': {'affected_scope': 'SKILL.md', 'reason': 'SYNTHETIC risk'}})
        case.sync('admission_decision', final)

    def test_rights_terminal_worksheet_tamper_is_rejected(self):
        t = self.case
        t.form(complete=True)
        t.sync('rights_review', 'approved-scope')
        t.form(changes={'rights_review': {'hosting-scope': 'https://example.invalid/tampered-rights'}})
        self.assertTrue(w.validate_record(t.root, t.record()))

    def test_engineering_terminal_worksheet_tamper_is_rejected(self):
        t = self.case
        t.form(complete=True)
        t.sync('engineering_review', 'passed')
        t.form(changes={'engineering_review': {'engineering-checks': 'https://example.invalid/tampered-engineering'}})
        self.assertTrue(w.validate_record(t.root, t.record()))

    def test_admission_terminal_worksheet_tamper_cannot_be_archived(self):
        t = self.case
        self.complete(t)
        t.form(changes={'admission_decision': {'scope-and-purpose': 'SYNTHETIC changed final purpose'}})
        self.assertTrue(w.validate_record(t.root, t.record()))
        self.assert_archive_refused_unchanged(t)

    def test_terminal_rejections_and_decline_protect_their_sections(self):
        for axis, decision, field in [('rights_review', 'rejected', 'hosting-scope'),
                                      ('engineering_review', 'rejected', 'dedup'),
                                      ('admission_decision', 'declined', 'scope-and-purpose')]:
            with self.subTest(axis=axis):
                t = self.new_case()
                t.form(complete=True)
                t.sync(axis, decision)
                t.form(changes={axis: {field: 'SYNTHETIC changed signed reason'}})
                self.assertTrue(w.validate_record(t.root, t.record()))

    def test_suspended_scope_and_reason_are_signed_evidence(self):
        for field, value in [('reason', 'SYNTHETIC changed risk'), ('affected_scope', '')]:
            with self.subTest(field=field):
                t = self.new_case()
                self.complete(t, 'suspended')
                t.form(changes={'suspension': {field: value}})
                self.assertTrue(w.validate_record(t.root, t.record()))
                self.assert_archive_refused_unchanged(t)

    def test_cross_role_signing_preserves_existing_signatures(self):
        t = self.case
        t.form(complete=True)
        t.sync('rights_review', 'approved-scope')
        original = self.files(t)
        t.form(changes={'engineering_review': {'dedup': 'https://example.invalid/new-dedup'},
                        'signature': {'credential_evidence_ref': 'controlled://synthetic/engineer'}})
        self.assertEqual(w.validate_record(t.root, t.record()), [])
        t.sync('engineering_review', 'passed')
        t.start()
        t.form(changes={'signature': {'credential_evidence_ref': 'controlled://synthetic/lawyer'}})
        t.sync('professional_review', 'approved-scope')
        t.form(changes={'admission_decision': {'scope-and-purpose': 'SYNTHETIC final independent purpose'},
                        'signature': {'credential_evidence_ref': 'controlled://synthetic/maintainer'}})
        t.sync('admission_decision', 'admitted')
        self.assertEqual(w.validate_record(t.root, t.record(), True, t.api), [])
        for name, content in original.items():
            if name.startswith('history/'):
                self.assertEqual((t.directory / name).read_bytes(), content)
        w.archive(t.root, t.rid)
        self.assertTrue(t.record()['archived'])

    def test_verified_same_role_rereview_can_update_its_own_evidence(self):
        for axis, decision, field in [('rights_review', 'approved-scope', 'hosting-scope'),
                                      ('engineering_review', 'passed', 'dedup'),
                                      ('admission_decision', 'declined', 'scope-and-purpose')]:
            with self.subTest(axis=axis):
                t = self.new_case()
                t.form(complete=True)
                t.sync(axis, decision)
                original = self.files(t)
                t.form(changes={axis: {field: 'https://example.invalid/renewed-evidence'}})
                self.assertTrue(w.validate_record(t.root, t.record()))
                t.sync(axis, decision)
                self.assertEqual(w.validate_record(t.root, t.record(), True, t.api), [])
                self.assertEqual(t.record()[axis]['gate_evidence'][field], 'https://example.invalid/renewed-evidence')
                for name, content in original.items():
                    if name.startswith('history/'):
                        self.assertEqual((t.directory / name).read_bytes(), content)

    def test_needs_changes_can_be_corrected_and_resigned(self):
        for axis, decision in [('rights_review', 'approved-scope'), ('engineering_review', 'passed')]:
            with self.subTest(axis=axis):
                t = self.new_case()
                t.form()
                t.sync(axis, 'needs-changes')
                t.form(complete=True)
                self.assertEqual(w.validate_record(t.root, t.record()), [])
                t.sync(axis, decision)
                self.assertEqual(w.validate_record(t.root, t.record(), True, t.api), [])

    def test_new_event_cannot_launder_another_roles_changed_evidence(self):
        t = self.case
        t.form(complete=True)
        t.sync('rights_review', 'approved-scope')
        t.form(changes={'rights_review': {'hosting-scope': 'https://example.invalid/tampered'}})
        url = t.event('engineering_review', 'passed')
        content = (t.directory / 'workbook.md').read_text()
        event = w.verify_event(url, w.binding(t.record(), content), t.rid, t.api)
        before = self.files(t)
        with self.assertRaises(w.ReviewError):
            w.apply_event(t.root, t.record(), content, event)
        with self.assertRaises(w.ReviewError):
            w.sync_event(t.root, t.rid, url, t.api)
        self.assertEqual(self.files(t), before)

    def test_unverified_same_role_event_cannot_unfreeze_terminal_evidence(self):
        t = self.case
        t.form(complete=True)
        t.sync('rights_review', 'approved-scope')
        t.form(changes={'rights_review': {'hosting-scope': 'https://example.invalid/unverified'}})
        before = self.files(t)
        with self.assertRaises(w.ReviewError):
            w.sync_event(t.root, t.rid, t.event('rights_review', 'approved-scope', '0'*64), t.api)
        self.assertTrue(w.validate_record(t.root, t.record()))
        self.assertEqual(self.files(t), before)

    def test_professional_maintenance_is_frozen_not_the_next_signers_identity(self):
        t = self.case
        t.approve_professional()
        t.form(changes={'signature': {'credential_evidence_ref': 'controlled://synthetic/next-role'}})
        self.assertEqual(w.validate_record(t.root, t.record()), [])
        t.form(changes={'maintenance': {'next_review_date': '2098-01-01'}})
        self.assertTrue(w.validate_record(t.root, t.record()))

    def test_professional_approval_alone_cannot_archive(self):
        t = self.case
        t.approve_professional()
        self.assert_archive_refused_unchanged(t)
        self.assertFalse((t.directory / 'archive.json').exists())

    def test_each_incomplete_independent_decision_blocks_archive(self):
        states = [('pending', 'passed', 'declined'), ('approved-scope', 'pending', 'declined'),
                  ('needs-changes', 'passed', 'declined'), ('approved-scope', 'needs-changes', 'declined'),
                  ('approved-scope', 'passed', 'not-admitted')]
        for rights, engineering, admission in states:
            with self.subTest(states=(rights, engineering, admission)):
                t = self.new_case()
                t.approve_professional()
                for axis, state in [('rights_review', rights), ('engineering_review', engineering), ('admission_decision', admission)]:
                    if state not in ('pending', 'not-admitted'):
                        t.sync(axis, state)
                self.assert_archive_refused_unchanged(t)

    def test_complete_independent_decisions_allow_archive(self):
        for final in ('admitted', 'declined', 'suspended'):
            with self.subTest(final=final):
                t = self.new_case()
                self.complete(t, final)
                w.archive(t.root, t.rid)
                self.assertTrue(t.record()['archived'])
                self.assertEqual(w.validate_record(t.root, t.record(), True, t.api), [])
        t = self.new_case()
        t.approve_professional()
        t.sync('rights_review', 'rejected')
        t.sync('engineering_review', 'rejected')
        t.sync('admission_decision', 'declined')
        w.archive(t.root, t.rid)
        self.assertEqual(w.validate_record(t.root, t.record(), True, t.api), [])

    def test_professional_rejection_can_archive_with_other_dimensions_pending(self):
        t = self.case
        t.start()
        t.form(changes={'C05': {'check_status': 'fail', 'finding': 'SYNTHETIC refusal'}})
        t.sync('professional_review', 'rejected')
        w.archive(t.root, t.rid)
        self.assertTrue(t.record()['archived'])
        self.assertEqual(t.record()['admission_decision']['status'], 'not-admitted')
        self.assertEqual(w.validate_record(t.root, t.record(), True, t.api), [])

    def test_idempotent_archive_also_checks_signed_workbook(self):
        t = self.case
        self.complete(t)
        w.archive(t.root, t.rid)
        t.form(changes={'rights_review': {'hosting-scope': 'https://example.invalid/post-archive-tamper'}})
        self.assert_archive_refused_unchanged(t)

    def test_archive_write_failure_preserves_original_and_removes_partial_bundle(self):
        t = self.case
        self.complete(t)
        before = self.files(t)
        replace = Path.replace
        def fail_record_commit(source, target):
            if Path(target) == t.directory / 'record.json':
                raise OSError('SYNTHETIC record commit failure')
            return replace(source, target)
        with mock.patch.object(Path, 'replace', fail_record_commit):
            with self.assertRaises(OSError):
                w.archive(t.root, t.rid)
        self.assertEqual(self.files(t), before)
        self.assertFalse((t.directory / 'archive.json').exists())
        self.assertEqual(w.validate_record(t.root, t.record()), [])
    def test_replayed_event_cannot_bypass_terminal_consistency(self):
        t = self.case
        t.form(complete=True)
        url = t.sync('rights_review', 'approved-scope')
        t.form(changes={'rights_review': {'hosting-scope': 'https://example.invalid/changed-on-replay'}})
        before = self.files(t)
        with self.assertRaises(w.ReviewError):
            w.sync_event(t.root, t.rid, url, t.api)
        self.assertEqual(self.files(t), before)

    def test_archive_staging_failure_has_no_side_effects(self):
        t = self.case
        self.complete(t)
        before = self.files(t)
        write = w.write
        def fail_staging(path, value):
            if Path(path).name == 'record.json':
                raise OSError('SYNTHETIC staging failure')
            return write(path, value)
        with mock.patch.object(w, 'write', fail_staging):
            with self.assertRaises(OSError):
                w.archive(t.root, t.rid)
        self.assertEqual(self.files(t), before)
        self.assertFalse((t.directory / 'archive.json').exists())
        self.assertEqual(w.validate_record(t.root, t.record()), [])


if __name__ == '__main__':
    unittest.main()
