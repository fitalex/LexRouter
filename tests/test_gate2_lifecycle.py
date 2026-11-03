"""Cross-Gate transitions use synthetic events in memory only."""
from copy import deepcopy
import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from test_gate2_adaptation import select_bundle
import test_review_workbench_v2 as fixtures
from test_review_workbench_v2 import FakeAPI, w


class GateLifecycleTests(unittest.TestCase):
    def test_sequential_merges_allow_multiple_bundles_without_scope_union(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for index in range(3):
                bundle = deepcopy(fixtures.bundle())
                bundle['review_id'] = f'RV-SYNTHETIC-{index}'
                path = root / w.review_path(bundle['review_id'], 'bundle')
                path.parent.mkdir(parents=True)
                path.write_text(json.dumps(bundle))
                selected = select_bundle(root, 'RV-SYNTHETIC-0')
                self.assertEqual(selected['review_scope'], ['SKILL.md'])
                self.assertEqual(selected['review_id'], 'RV-SYNTHETIC-0')
            with self.assertRaises(FileNotFoundError):
                select_bundle(root, 'RV-MISSING')

    def test_infrastructure_merge_then_candidate_sync_keeps_signing_fail_closed(self):
        api = FakeAPI()
        row = {'path': 'tests/test_gate2_adaptation.py', 'sha': 'f' * 40,
               'mode': '100644', 'type': 'blob'}
        api.ci_trees[fixtures.MAIN] = {'truncated': False, 'tree': []}
        api.ci_trees[fixtures.HEAD] = {'truncated': False, 'tree': []}
        w.verify_anchors(api, api.b, fixtures.HEAD, fixtures.MAIN)
        api.ci_trees[fixtures.MAIN]['tree'] = [row]
        with self.assertRaises(w.ReviewError):
            w.verify_anchors(api, api.b, fixtures.HEAD, fixtures.MAIN)
        api.ci_trees[fixtures.HEAD]['tree'] = [deepcopy(row)]
        w.verify_anchors(api, api.b, fixtures.HEAD, fixtures.MAIN)

    def test_credentials_then_signed_history_then_closed_pr(self):
        api = FakeAPI()
        credential = deepcopy(api.policy['credential_refs'])
        api.policy['credential_refs'] = {}
        with self.assertRaises(w.ReviewError):
            api.sync()
        api.policy['credential_refs'] = credential
        ledger = api.sync()
        self.assertEqual(len(ledger['entries']), 1)
        api, ledger = fixtures.SecurityRegressionTests().signed_fixture()
        self.assertEqual(w.verify_saved_history(api.b, ledger, api), ledger)
        api.pr_state = 'closed'
        self.assertEqual(w.verify_saved_history(api.b, ledger, api), ledger)

    def test_signed_history_rejects_tamper_and_deletion(self):
        api, ledger = fixtures.SecurityRegressionTests().signed_fixture()
        changed = deepcopy(ledger)
        changed['entries'][0]['actor'] = 'SYNTHETIC-forged'
        with self.assertRaises(w.ReviewError):
            w.verify_saved_history(api.b, changed, api)
        with self.assertRaises(w.ReviewError):
            w.validate_ledger(w.empty_ledger(api.b), api.b, ledger)

    def test_registered_credentials_do_not_waive_missing_evidence(self):
        api = FakeAPI()
        api.b['matrix'][0]['facts'] = 'not-verified'
        with self.assertRaises(w.ReviewError):
            api.sync()
