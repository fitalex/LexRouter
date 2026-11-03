"""Nine Gate 2 candidate-data regressions; never submit Reviews or write ledgers.

Run explicitly with GATE2_REQUIRED=1 and GATE2_CANDIDATE_ROOT,
GATE2_BASE_REF, GATE2_HEAD_REF, GATE2_ORIGINAL_REF, GATE2_REVIEW_ID. Candidate checkout is data
only; production modules and synthetic authentication fixtures come from this
implementation checkout. The manifest adapter is an offline regression fixture,
not live identity authentication or legal approval.
"""
import base64
from copy import deepcopy
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import re
import os
import shutil
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest

# Execute only the implementation checkout's modules, never candidate Python.
IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(IMPLEMENTATION_ROOT / 'scripts'), str(IMPLEMENTATION_ROOT / 'tests')]
import review_workbench_v2 as w
from test_review_workbench_v2 import FakeAPI
from unittest import mock

ROOT = Path(os.environ.get('GATE2_CANDIDATE_ROOT', IMPLEMENTATION_ROOT)).resolve()
ENABLED = os.environ.get('GATE2_REQUIRED') == '1'


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()


MAIN = HEAD = ORIGINAL = None
CASES = []


def setUpModule():
    global MAIN, HEAD, ORIGINAL, CASES
    if not ENABLED:
        raise unittest.SkipTest('Gate 2 data regressions run in the dedicated candidate CI matrix')
    for key in ('GATE2_BASE_REF', 'GATE2_HEAD_REF', 'GATE2_ORIGINAL_REF', 'GATE2_REVIEW_ID'):
        if not os.environ.get(key):
            raise AssertionError(f'{key} is required; candidate selection must be explicit')
    MAIN = git('rev-parse', os.environ['GATE2_BASE_REF'] + '^{commit}')
    HEAD = git('rev-parse', os.environ['GATE2_HEAD_REF'] + '^{commit}')
    ORIGINAL = git('rev-parse', os.environ['GATE2_ORIGINAL_REF'] + '^{commit}')
    if git('rev-parse', 'HEAD') != HEAD:
        raise AssertionError('Candidate checkout is not the selected immutable head')
    if git('status', '--porcelain', '--untracked-files=no'):
        raise AssertionError('Candidate tracked data must be clean')
    rid = os.environ['GATE2_REVIEW_ID']
    if not re.fullmatch(r'RV-[A-Za-z0-9-]+', rid):
        raise AssertionError('Invalid selected Review ID')
    CASES = [(rid, select_bundle(ROOT, rid))]
    print(f'Gate 2 candidate={rid} head={HEAD} accepted_baseline={MAIN} original_v1_snapshot={ORIGINAL}', flush=True)


def select_bundle(root, rid):
    bundle = w.loads((root / w.review_path(rid, 'bundle')).read_text())
    w.require(bundle['review_id'] == rid, 'Selected bundle identity differs')
    return bundle


def subject(bundle):
    return w.loads(git('show', MAIN + ':' + bundle['subject_ref']))


def tree(ref):
    rows = []
    for line in git('ls-tree', '-r', ref).splitlines():
        meta, path = line.split('\t', 1)
        mode, kind, sha = meta.split()
        rows.append({'path': path, 'mode': mode, 'type': kind, 'sha': sha})
    return {'truncated': False, 'tree': rows}


def anchor_api(bundle):
    # Immutable main registry/manifest snapshots were checked against actual
    # GitHub trees during baseline capture. This adapter is a regression fixture,
    # not a claim to re-authenticate GitHub identities offline.
    manifest = w.loads(git('show', MAIN + ':' + subject(bundle)['scope_manifest_ref']))
    source = {'truncated': False, 'tree': [
        {'path': row['path'], 'sha': row['blob_sha'], 'mode': row['mode'],
         'type': 'commit' if row['mode'] == '160000' else 'blob'} for row in manifest['files']]}
    def api(path, method='GET', payload=None):
        if method != 'GET':
            raise AssertionError('Regression fixtures never write GitHub data')
        prefix = w.PREFIX + '/contents/'
        if path.startswith(prefix):
            name, ref = path[len(prefix):].split('?ref=')
            if ref != MAIN:
                raise AssertionError('Unexpected registry baseline')
            raw = git('show', ref + ':' + name).encode()
            return {'type': 'file', 'encoding': 'base64', 'content': base64.b64encode(raw).decode()}
        if path == f'repos/{bundle["source_repository"]}/git/trees/{bundle["source_revision"]}?recursive=1':
            return deepcopy(source)
        if path == f'{w.PREFIX}/git/trees/{MAIN}?recursive=1':
            return tree(MAIN)
        if path == f'{w.PREFIX}/git/trees/{HEAD}?recursive=1':
            return tree(HEAD)
        raise AssertionError('Unexpected read-only anchor query')
    return api


def complete_fixture(bundle, na=False):
    result = deepcopy(bundle)
    for row in result['matrix']:
        row.update(authority_refs=['https://example.invalid/SYNTHETIC-authority'],
                   evidence_refs=['controlled://SYNTHETIC/facts'])
        for key in ('facts', 'effective_period', 'transitional_rule', 'applicability'):
            row[key] = 'SYNTHETIC complete engineering fixture; not a real legal finding'
        if na:
            row['not_applicable_reason'] = 'SYNTHETIC absent predicate with item-specific evidence'
    result['rights_evidence'] = {key: [{'ref': 'controlled://SYNTHETIC/rights', 'status': 'verified',
                                      'summary': 'SYNTHETIC fixture only'}] for key in w.GATES[result['track']]}
    result['validity']['next_review_date'] = (date.today() + timedelta(days=30)).isoformat()
    text = (w.render_form(result).replace('<decision>', 'not-applicable' if na else 'approved-scope')
            .replace('Decision: not-applicable', 'Decision: approved-scope')
            .replace('<reason>', 'SYNTHETIC reasoning').replace('<limitations>', 'SYNTHETIC limits')
            .replace('<personal declaration>', 'SYNTHETIC COI')
            .replace('<actual YYYY-MM-DD>', date.today().isoformat()))
    return result, w.parse_form(text)


def check_gates(bundle, form):
    def api(path):
        assert '/check-runs?' in path
        return {'check_runs': [{'id': 1, 'name': 'SYNTHETIC-CI', 'app': {'id': 15368},
                               'head_sha': HEAD, 'status': 'completed', 'conclusion': 'success'}]}
    w.ensure_gates(api, bundle, form, w.empty_ledger(bundle), HEAD,
                   {'policy': {'ci_required': ['SYNTHETIC-CI'], 'ci_app_id': 15368,
                               'max_regulatory_age_days': 90}})


def compatibility_files(name):
    path = ROOT / 'docs/review-workbench/v2/gate2' / name.removeprefix('RV-20261017-') / 'compatibility.md'
    block = re.search(r'```json\n(.*?)\n```', git('show', ORIGINAL + ':' + str(path.relative_to(ROOT))), re.S)
    assert block, 'Missing captured v1 digest map'
    return json.loads(block[1])['original_files']


def verify_originals(rows, root=ROOT):
    if not rows:
        raise AssertionError('Captured originals must not be empty')
    for row in rows:
        path = root / w.safe_path(row['path'])
        if not row['path'].startswith('data/reviews/cases/' + os.environ['GATE2_REVIEW_ID'] + '/'):
            continue
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError('Captured v1 original changed')


def verify_original_inventory(rows):
    def inventory(ref):
        return {row['path']: (row['sha'], row['mode'], row['type'])
                for row in tree(ref)['tree'] if row['path'].startswith('data/reviews/cases/')}
    original = inventory(ORIGINAL)
    current = inventory(HEAD)
    target = 'data/reviews/cases/' + os.environ['GATE2_REVIEW_ID'] + '/'
    if not original or any(current.get(p) != v for p, v in original.items() if p.startswith(target)):
        raise ValueError('Complete captured v1 inventory or Git blobs changed')
    if len(rows) != len(original) or {row['path'] for row in rows} != set(original):
        raise ValueError('Compatibility map must cover every original v1 file exactly once')
    for row in rows:
        if row['git_blob'] != original[row['path']][0]:
            raise ValueError('Compatibility map Git blob differs from immutable original')
        baseline = subprocess.check_output(['git', '-C', str(ROOT), 'show', ORIGINAL + ':' + w.safe_path(row['path'])])
        if hashlib.sha256(baseline).hexdigest() != row['sha256']:
            raise ValueError('Compatibility map digest differs from immutable original')


class Gate2AdaptationTests(unittest.TestCase):
    def test_real_bundle_full_matrix_and_authenticated_ledger(self):
        self.assertTrue(CASES, 'No candidate bundle found')
        for rid, bundle in CASES:
            with self.subTest(review=rid):
                w.validate_bundle(bundle)
                self.assertEqual(set(bundle['review_scope']), set(subject(bundle)['review_scope']))
                ledger = w.loads((ROOT / w.review_path(rid, 'ledger')).read_text())
                baseline_path = MAIN + ':' + w.review_path(rid, 'ledger')
                baseline_raw = subprocess.run(['git', '-C', str(ROOT), 'show', baseline_path], capture_output=True, text=True)
                baseline = w.loads(baseline_raw.stdout) if baseline_raw.returncode == 0 else None
                w.validate_ledger(ledger, bundle, baseline)
                for key in ('source_revision', 'source_repository', 'source_manifest', 'review_scope', 'excluded_scope', 'template_versions'):
                    snapshot = w.loads(git('show', ORIGINAL + ':' + w.review_path(rid, 'bundle')))
                    self.assertEqual(bundle[key], snapshot[key])
                if os.environ.get('GATE2_PR'):
                    w.immutable_history(w.github_api, int(os.environ['GATE2_PR']), bundle, ledger)
                if ledger['entries']:
                    w.verify_saved_history(bundle, ledger, active=os.environ.get('GATE2_ACTIVE', 'true') == 'true')

    def test_actual_unverified_evidence_cannot_approve(self):
        for rid, current in CASES:
            bundle = w.loads(git('show', ORIGINAL + ':' + w.review_path(rid, 'bundle')))
            _, form = complete_fixture(bundle)
            with self.subTest(review=rid), self.assertRaises(w.ReviewError):
                check_gates(bundle, form)

    def test_missing_authority_fact_or_time_blocks_each_candidate(self):
        for rid, original in CASES:
            for field, value in (('authority_refs', []), ('evidence_refs', []),
                                 ('facts', 'not-verified'), ('effective_period', 'not-verified'),
                                 ('transitional_rule', 'not-verified')):
                bundle, form = complete_fixture(original)
                bundle['matrix'][-1][field] = value
                with self.subTest(review=rid, field=field), self.assertRaises(w.ReviewError):
                    check_gates(bundle, form)

    def test_missing_per_item_not_applicable_reason_blocks(self):
        for rid, original in CASES:
            bundle, form = complete_fixture(original, na=True)
            check_gates(bundle, form)
            bundle['matrix'][-1].pop('not_applicable_reason')
            with self.subTest(review=rid), self.assertRaises(w.ReviewError):
                check_gates(bundle, form)

    def test_source_manifest_or_scope_changes_are_rejected(self):
        # Strict executable closure belongs to the fixed Gate 2 snapshot.
        # Activity checks above validate pinned source and authenticate every saved event.
        with mock.patch.dict(globals(), MAIN='d1c7ebabd5c33d2e92c6916804adc4018c89e5a0', HEAD=ORIGINAL):
            for rid, current in CASES:
                original = w.loads(git('show', ORIGINAL + ':' + w.review_path(rid, 'bundle')))
                w.verify_anchors(anchor_api(original), original, HEAD, MAIN)
                for change in ('source', 'manifest', 'scope'):
                    bundle = deepcopy(original)
                    if change == 'source':
                        bundle['source_revision'] = '0' * 40
                    elif change == 'manifest':
                        bundle['source_manifest'][0]['blob_sha'] = '0' * 40
                    else:
                        bundle['review_scope'].pop()
                    with self.subTest(review=rid, change=change), self.assertRaises(w.ReviewError):
                        w.verify_anchors(anchor_api(original), bundle, HEAD, MAIN)
                # The shared harness does not weaken the production main/code closure.
                real_api = anchor_api(original)
                def changed_code_api(path, method='GET', payload=None):
                    response = real_api(path, method, payload)
                    if path == f'{w.PREFIX}/git/trees/{HEAD}?recursive=1':
                        response = deepcopy(response)
                        for row in response['tree']:
                            if row['path'] == 'scripts/review_workbench_v2.py':
                                row['sha'] = '0' * 40
                                break
                        else:
                            raise AssertionError('Protected implementation missing from candidate tree')
                    return response
                with self.subTest(review=rid, change='protected-code'), self.assertRaises(w.ReviewError):
                    w.verify_anchors(changed_code_api, original, HEAD, MAIN)

    def test_fake_signature_or_identity_authorization_is_rejected(self):
        for change in ('bot', 'permission', 'role', 'credential'):
            api = FakeAPI()
            if change == 'bot':
                api.events[1]['user']['type'] = 'Bot'
            elif change == 'permission':
                api.permission = 'read'
            elif change == 'role':
                api.roles['reviewers'] = {}
            else:
                api.policy['credential_refs'] = {}
            with self.subTest(change=change), self.assertRaises(w.ReviewError):
                w.authenticate(api, 7, api.events[1], 'synthetic-human',
                               {'roles': api.roles, 'policy': api.policy})
            self.assertEqual(api.writes, [])

    def test_v1_captured_bytes_and_history_are_preserved(self):
        for rid, _ in CASES:
            rows = compatibility_files(rid)
            verify_originals([row for row in rows if row['path'].startswith('data/reviews/cases/' + rid + '/')])
            verify_original_inventory(rows)

    def test_v1_original_deletion_or_rewrite_is_detected(self):
        for rid, _ in CASES:
            rows = compatibility_files(rid)
            with self.subTest(review=rid, change='omitted-captured-file'), self.assertRaises(ValueError):
                verify_original_inventory(rows[1:])
            target = next(row['path'] for row in rows if row['path'].startswith('data/reviews/cases/' + rid + '/'))
            for change in ('deleted', 'rewritten'):
                # Mutate only a disposable copy of the real captured files.
                with TemporaryDirectory(prefix='gate2-originals-') as directory:
                    root = Path(directory)
                    for row in rows:
                        if not row['path'].startswith('data/reviews/cases/' + rid + '/'):
                            continue
                        source = ROOT / w.safe_path(row['path'])
                        destination = root / row['path']
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(source, destination)
                    verify_originals([row for row in rows if row['path'].startswith('data/reviews/cases/' + rid + '/')], root)
                    path = root / target
                    if change == 'deleted':
                        path.unlink()
                    else:
                        path.write_bytes(path.read_bytes() + b'\nSYNTHETIC tampering')
                    with self.subTest(review=rid, change=change), self.assertRaises((ValueError, FileNotFoundError)):
                        verify_originals([row for row in rows if row['path'].startswith('data/reviews/cases/' + rid + '/')], root)

    def test_empty_gate2_snapshot_and_accepted_current_policy(self):
        policy = w.loads(git('show', MAIN + ':' + w.POLICY_PATH))
        self.assertEqual(policy['repository'], w.REPOSITORY)
        baseline_policy = w.loads(git('show', ORIGINAL + ':' + w.POLICY_PATH))
        self.assertEqual(baseline_policy['credential_refs'], {})
        for rid, bundle in CASES:
            ledger = w.loads(git('show', ORIGINAL + ':' + w.review_path(rid, 'ledger')))
            self.assertEqual(ledger['entries'], [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
