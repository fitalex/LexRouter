from copy import deepcopy
import unittest
from gate2_refs import resolve


class ReferenceLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.pr = {'number': 9, 'state': 'open', 'merged': False,
                   'base': {'ref': 'main', 'repo': {'full_name': 'fitalex/LexRouter'}},
                   'head': {'sha': 'a' * 40}, 'merge_commit_sha': 'c' * 40}

    def test_open_event_binds_triggering_sha(self):
        self.assertEqual(resolve(self.pr, 'b' * 40, '9', 'd' * 40)['head'], 'd' * 40)

    def test_closed_deleted_branch_uses_retained_head_commit(self):
        self.pr.update(state='closed', head={'sha': 'a' * 40, 'repo': None})
        result = resolve(self.pr, 'b' * 40)
        self.assertEqual((result['head'], result['active']), ('a' * 40, 'false'))

    def test_merged_pr_uses_merge_snapshot_after_branch_deletion(self):
        self.pr.update(state='closed', merged=True, head={'repo': None})
        self.assertEqual(resolve(self.pr, 'b' * 40)['head'], 'c' * 40)

    def test_missing_snapshot_and_unknown_state_fail_instead_of_skip(self):
        for change in ({'state': 'closed', 'merged': True, 'merge_commit_sha': None}, {'state': 'unknown'}):
            pr = deepcopy(self.pr)
            pr.update(change)
            with self.assertRaises(ValueError):
                resolve(pr, 'b' * 40)
