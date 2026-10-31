# Gate 2 候选适配正反测试

这些测试读取当前分支真实bundle及空ledger，并在内存副本中构造明确标注的SYNTHETIC反例。不创建Review、不写GitHub、不把合成权利/日期/身份写入真实附件。主仓现有168项测试继续由GitHub CI执行；本附加9项候选数据回归在本地执行，输出附各候选TEST_OUTPUT.md。

源树adapter只使用已在线比对的main固定manifest作可重复回归夹具，不声称离线认证GitHub身份。真实v1/v2在线入口另外执行；0事件不等于真人签署验收。

从仓库根提取以下唯一Python代码块到临时文件，以 `python 临时文件.py` 执行即可重跑；无需修改生产脚本或信任PR中的可执行代码。

```python
"""Gate 2 candidate-data regressions. No Review submission or ledger writes."""
import base64
from copy import deepcopy
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path.cwd()
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'tests')]
import review_workbench_v2 as w
from test_review_workbench_v2 import FakeAPI


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


MAIN = git('rev-parse', 'origin/main')
HEAD = git('rev-parse', 'HEAD')
CASES = [(p.parent.name, w.loads(p.read_text()))
         for p in sorted((ROOT / 'data/reviews/v2').glob('RV-*/bundle.json'))]


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
    block = re.search(r'```json\n(.*?)\n```', path.read_text(), re.S)
    assert block, 'Missing captured v1 digest map'
    return json.loads(block[1])['original_files']


def verify_originals(rows, reader=lambda p: p.read_bytes()):
    for row in rows:
        raw = reader(ROOT / row['path'])
        if hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError('Captured v1 original changed')


class Gate2AdaptationTests(unittest.TestCase):
    def test_real_bundle_full_matrix_and_empty_ledger(self):
        self.assertTrue(CASES, 'No candidate bundle found')
        for rid, bundle in CASES:
            with self.subTest(review=rid):
                w.validate_bundle(bundle)
                self.assertEqual(set(bundle['review_scope']), set(subject(bundle)['review_scope']))
                ledger = w.loads((ROOT / w.review_path(rid, 'ledger')).read_text())
                self.assertEqual(ledger, w.empty_ledger(bundle))

    def test_actual_unverified_evidence_cannot_approve(self):
        for rid, bundle in CASES:
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
        for rid, original in CASES:
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
            verify_originals(compatibility_files(rid))

    def test_v1_original_deletion_or_rewrite_is_detected(self):
        for rid, _ in CASES:
            rows = compatibility_files(rid)
            target = rows[0]['path']
            for change in ('deleted', 'rewritten'):
                def reader(path):
                    if path.relative_to(ROOT).as_posix() == target:
                        if change == 'deleted':
                            raise FileNotFoundError('SYNTHETIC deletion')
                        return path.read_bytes() + b'\nSYNTHETIC tampering'
                    return path.read_bytes()
                with self.subTest(review=rid, change=change), self.assertRaises((ValueError, FileNotFoundError)):
                    verify_originals(rows, reader)

    def test_policy_and_production_ledger_are_not_synthetic_signatures(self):
        policy = w.loads((ROOT / w.POLICY_PATH).read_text())
        self.assertEqual(policy, w.loads(git('show', MAIN + ':' + w.POLICY_PATH)))
        self.assertEqual(policy['credential_refs'], {})
        for rid, bundle in CASES:
            ledger = w.loads((ROOT / w.review_path(rid, 'ledger')).read_text())
            self.assertEqual(ledger['entries'], [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
```
