"""SYNTHETIC workflow trust-boundary tests; never submits a GitHub review."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import review_workbench_v2_sync_run as bridge


class SignalTests(unittest.TestCase):
    def setUp(self):
        repo = {'full_name': bridge.REPOSITORY}
        self.head = 'a' * 40
        self.run = {'id': 42, 'event': 'pull_request_review',
                    'path': bridge.SIGNAL_PATH, 'status': 'completed',
                    'conclusion': 'success', 'head_repository': repo,
                    'head_sha': self.head, 'pull_requests': [{'number': 7}]}
        self.pr = {'state': 'open', 'commits': 0, 'head': {'sha': self.head, 'ref': 'review/synthetic', 'repo': repo},
                   'base': {'ref': 'main', 'repo': repo}, 'merge_commit_sha': 'b' * 40}
        self.tree = {'truncated': False, 'tree': [
            {'path': 'data/reviews/v2/RV-synthetic/ledger.json',
             'type': 'blob', 'mode': '100644'}]}
        self.reviews = [{'id': 99, 'commit_id': self.head, 'state': 'COMMENTED',
                         'body': 'lexrouter-review-v2 SYNTHETIC',
                         'user': {'login': 'synthetic-human', 'type': 'User'}}]
        self.calls = []
        self.commits = []
        self.prior_trees = {}

    def api(self, path, method='GET', payload=None):
        self.calls.append(path)
        if path.endswith('/actions/runs/42'):
            return deepcopy(self.run)
        if path.endswith('/pulls/7'):
            return deepcopy(self.pr)
        if '/git/trees/' in path:
            sha = path.split('/git/trees/')[1].split('?')[0]
            if sha in self.prior_trees:
                return deepcopy(self.prior_trees[sha])
            return deepcopy(self.tree)
        if '/commits?' in path:
            return deepcopy(self.commits)
        if '/reviews?' in path:
            return deepcopy(self.reviews)
        if path.endswith('/dispatches'):
            self.assertEqual(method, 'POST')
            self.assertEqual(payload, {'ref': 'review/synthetic'})
            return None
        self.fail('Unexpected API request')

    def run_bridge(self):
        policy = {'roles': {'reviewers': {'synthetic-human': ['Legal Reviewer']}}}
        with patch.object(bridge.v2, 'main_sha', return_value='f' * 40), \
                patch.object(bridge.v2, 'policy_at', return_value=policy), \
                patch.object(bridge.v2, 'content_at', return_value=None), \
                patch.object(bridge.v2, 'authenticate'), \
                patch.object(bridge.v2, 'online_validate') as validate:
            with patch.object(bridge.v2, 'sync_review') as sync:
                result = bridge.sync_run(42, write=True, api=self.api)
                return result, validate, sync

    def test_valid_signal_rechecks_history_then_imports_current_event(self):
        result, validate, sync = self.run_bridge()
        self.assertEqual(result, 1)
        validate.assert_called_once_with(bridge.REPOSITORY, 7, 'RV-synthetic', api=self.api)
        sync.assert_called_once_with(bridge.REPOSITORY, 7, 99, 'synthetic-human',
                                     self.head, event_action='submitted', write=True, api=self.api)
        self.assertFalse(any('artifacts' in path for path in self.calls))
        self.assertTrue(any('/dispatches' in path for path in self.calls))

    def test_unassigned_public_comments_cannot_block_human_signature(self):
        self.reviews.extend([{**self.reviews[0], 'id': i,
                              'user': {'login': 'outsider', 'type': 'User'}} for i in (100, 101)])
        count, _, sync = self.run_bridge()
        self.assertEqual(count, 1)
        sync.assert_called_once()

    def test_signal_cannot_self_authorize_wrong_event_path_repo_or_pr(self):
        original = deepcopy(self.run)
        for field, value in [('event', 'push'), ('path', 'attacker.yml'),
                             ('conclusion', 'failure'), ('pull_requests', []),
                             ('head_repository', {'full_name': 'attacker/fork'})]:
            with self.subTest(field=field):
                self.run = {**original, field: value}
                with self.assertRaises(bridge.v2.ReviewError):
                    self.run_bridge()

    def test_fork_or_non_main_pr_rejected(self):
        self.pr['head']['repo'] = {'full_name': 'attacker/fork'}
        with self.assertRaises(bridge.v2.ReviewError):
            self.run_bridge()

    def test_edited_or_dismissed_history_failure_prevents_new_import(self):
        with patch.object(bridge.v2, 'main_sha', return_value='f' * 40), \
                patch.object(bridge.v2, 'content_at', return_value=None), \
                patch.object(bridge.v2, 'online_validate', side_effect=bridge.v2.ReviewError('changed')):
            with patch.object(bridge.v2, 'sync_review') as sync:
                with self.assertRaises(bridge.v2.ReviewError):
                    bridge.sync_run(42, write=True, api=self.api)
                sync.assert_not_called()

    def test_stale_signal_audits_history_and_retries_ci_without_importing(self):
        self.run['head_sha'] = 'c' * 40
        count, validate, sync = self.run_bridge()
        self.assertEqual(count, 0)
        validate.assert_called_once()
        sync.assert_not_called()

    def test_entire_unmerged_review_directory_deletion_is_detected(self):
        old = 'd' * 40
        self.commits = [{'sha': old}]
        self.pr['commits'] = 1
        self.prior_trees[old] = deepcopy(self.tree)
        self.tree['tree'] = []
        with self.assertRaises(bridge.v2.ReviewError):
            self.run_bridge()

    def test_truncated_commit_listing_cannot_hide_history(self):
        for total in (1, 251):
            self.pr['commits'] = total
            with self.assertRaises(bridge.v2.ReviewError):
                self.run_bridge()

    def test_concurrent_reviews_rejected_without_reordering(self):
        self.reviews.append({**self.reviews[0], 'id': 100})
        with self.assertRaises(bridge.v2.ReviewError):
            self.run_bridge()

    def test_dismissed_current_review_and_truncated_tree_rejected(self):
        self.reviews[0]['state'] = 'DISMISSED'
        with self.assertRaises(bridge.v2.ReviewError):
            self.run_bridge()
        self.tree['truncated'] = True
        with self.assertRaises(bridge.v2.ReviewError):
            self.run_bridge()

    def test_privileged_workflow_uses_only_trusted_code(self):
        root = Path(__file__).resolve().parents[1]
        privileged = (root / '.github/workflows/review-v2-sync.yml').read_text()
        signal = (root / '.github/workflows/review-v2-signal.yml').read_text()
        self.assertIn('workflow_run:', privileged)
        self.assertIn('ref: ${{ github.workflow_sha }}', privileged)
        self.assertIn('persist-credentials: false', privileged)
        self.assertNotIn('workflow_run.head_sha', privileged)
        self.assertNotIn('download-artifact', privileged)
        self.assertIn('permissions: {}', signal)
        self.assertNotIn('uses:', signal)


if __name__ == '__main__':
    unittest.main()
