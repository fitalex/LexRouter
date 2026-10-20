"""PR #15 P1 regression: SYNTHETIC inapplicability is never an evidence waiver."""
from copy import deepcopy
import unittest

from test_review_workbench_v2 import FakeAPI, HEAD, MAIN, w


def decision_text(api, na_groups, axis='professional_review', decision='approved-scope'):
    text = w.render_form(api.b, axis).replace('<decision>', 'approved-scope')
    text = text.replace('Decision: approved-scope', 'Decision: ' + decision)
    for gid in na_groups:
        text = text.replace(f'Group: {gid} | approved-scope', f'Group: {gid} | not-applicable')
    return (text.replace('<reason>', 'SYNTHETIC expert reason; see each file/check basis')
            .replace('<limitations>', 'SYNTHETIC limited scope')
            .replace('<personal declaration>', 'SYNTHETIC COI')
            .replace('<actual YYYY-MM-DD>', api.events[1]['submitted_at'][:10]))


def two_file_case(na_groups):
    api = FakeAPI()
    checks = api.b['groups'][0]['check_ids']
    api.b['groups'] = [
        {'group_id': 'G1', 'label': 'SYNTHETIC common facts', 'check_ids': checks[:5]},
        {'group_id': 'G2', 'label': 'SYNTHETIC special circumstances', 'check_ids': checks[5:]},
    ]
    for row in api.b['matrix']:
        row['group_id'] = 'G1' if row['check_id'] in checks[:5] else 'G2'
    api.b['review_scope'].append('references/example.md')
    api.b['source_manifest'].append({'path': 'references/example.md', 'blob_sha': 'e' * 40})
    api.source_tree['tree'].append({'path': 'references/example.md', 'sha': 'e' * 40,
                                   'type': 'blob', 'mode': '100644'})
    api.b['matrix'] += [{**deepcopy(row), 'file': 'references/example.md'} for row in api.b['matrix']]
    for row in api.b['matrix']:
        if row['group_id'] in na_groups:
            row['facts'] = 'SYNTHETIC evidence establishes that the regulated event did not occur.'
            row['applicability'] = 'SYNTHETIC cited rule requires that event; its predicate is absent.'
            row['not_applicable_reason'] = (
                f'SYNTHETIC {row["file"]}/{row["check_id"]}: the documented absent event '
                'means the cited rule does not apply; no broader exemption is asserted.')
    api.events[1]['body'] = decision_text(api, na_groups)
    return api


class InapplicabilityTests(unittest.TestCase):
    def assert_no_import(self, api):
        before = deepcopy(api.ledger)
        with self.assertRaises(w.ReviewError):
            api.sync(write=True)
        self.assertEqual(api.ledger, before)
        self.assertEqual(api.writes, [])

    def test_all_groups_not_applicable_without_authorities_or_evidence_blocked(self):
        api = two_file_case({'G1', 'G2'})
        for row in api.b['matrix']:
            row['authority_refs'] = []
            row['evidence_refs'] = []
        self.assert_no_import(api)

    def test_partial_not_applicable_missing_any_file_check_evidence_blocked(self):
        # Cover every NA row, including the second file; a valid first group or
        # another complete row in the same group cannot mask the missing row.
        for index in range(20):
            for field in ('authority_refs', 'evidence_refs'):
                api = two_file_case({'G2'})
                if api.b['matrix'][index]['group_id'] != 'G2':
                    continue
                api.b['matrix'][index][field] = []
                with self.subTest(row=index, field=field):
                    self.assert_no_import(api)

    def test_missing_or_unresolved_per_check_inapplicability_basis_blocked(self):
        for field in ('facts', 'effective_period', 'transitional_rule', 'applicability', 'not_applicable_reason'):
            for value in ('', 'not-verified', '待核', '〈待填写〉'):
                api = two_file_case({'G2'})
                api.b['matrix'][-1][field] = value
                with self.subTest(field=field, value=value):
                    self.assert_no_import(api)
        api = two_file_case({'G2'})
        del api.b['matrix'][-1]['not_applicable_reason']
        self.assert_no_import(api)

    def test_structured_basis_permits_all_or_partial_inapplicability_and_independent_admission(self):
        for na_groups in ({'G1', 'G2'}, {'G2'}, set()):
            with self.subTest(na_groups=na_groups):
                api = two_file_case(na_groups)
                first = api.sync()
                api.ledger = first
                api.snapshots[(HEAD, w.review_path(api.b['review_id'], 'ledger'))] = w.empty_ledger(api.b)
                api.head = 'e' * 40
                api.checks_by_head[HEAD] = deepcopy(api.checks)
                api.checks[0]['head_sha'] = api.head
                api.events[2] = {**api.events[1], 'id': 2, 'node_id': 'SYNTHETIC-REVIEW-NODE-2',
                    'commit_id': api.head, 'body': decision_text(api, na_groups, 'admission_decision', 'admitted'),
                    'html_url': 'https://github.com/fitalex/LexRouter/pull/7#pullrequestreview-2'}
                result = api.sync(review_number=2)
                self.assertEqual(result['entries'][:1], first['entries'])
                self.assertEqual(result['entries'][-1]['form']['decision'], 'admitted')
                self.assertEqual([entry['event_id'] for entry in result['entries']], [1, 2])

    def test_admission_cannot_use_not_applicable_to_avoid_row_basis(self):
        api = two_file_case(set())
        api.ledger = api.sync()
        api.snapshots[(HEAD, w.review_path(api.b['review_id'], 'ledger'))] = w.empty_ledger(api.b)
        api.head = 'e' * 40
        api.checks_by_head[HEAD] = deepcopy(api.checks)
        api.checks[0]['head_sha'] = api.head
        api.events[2] = {**api.events[1], 'id': 2, 'node_id': 'SYNTHETIC-REVIEW-NODE-2',
            'commit_id': api.head, 'body': decision_text(api, {'G2'}, 'admission_decision', 'admitted'),
            'html_url': 'https://github.com/fitalex/LexRouter/pull/7#pullrequestreview-2'}
        with self.assertRaises(w.ReviewError):
            api.sync(review_number=2, write=True)
        self.assertEqual(api.writes, [])
        self.assertEqual(len(api.ledger['entries']), 1)

    def test_handcrafted_old_bypass_ledger_is_rejected_by_history_replay(self):
        api = two_file_case({'G1', 'G2'})
        for row in api.b['matrix']:
            row['authority_refs'] = []
            row['evidence_refs'] = []
        trusted = {'roles': api.roles, 'policy': api.policy}
        ledger = w.append_event(api.b, w.empty_ledger(api.b), api.events[1],
            w.parse_form(api.events[1]['body']), 'synthetic-human', 7, MAIN, trusted)
        api.snapshots[(HEAD, w.review_path(api.b['review_id'], 'ledger'))] = w.empty_ledger(api.b)
        with self.assertRaises(w.ReviewError):
            w.verify_saved_history(api.b, ledger, api)
        self.assertEqual(api.writes, [])

    def test_needs_changes_can_still_record_unresolved_inapplicability(self):
        api = two_file_case({'G1', 'G2'})
        for row in api.b['matrix']:
            row['authority_refs'] = []
            row['evidence_refs'] = []
            row.pop('not_applicable_reason')
        api.events[1]['body'] = decision_text(api, {'G1', 'G2'}, decision='needs-changes')
        result = api.sync()
        self.assertEqual(result['entries'][0]['form']['decision'], 'needs-changes')


if __name__ == '__main__':
    unittest.main()
