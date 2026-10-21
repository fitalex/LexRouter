"""Gate1 v2 regressions. Every actor, event and legal statement is SYNTHETIC."""
import base64
from copy import deepcopy
from datetime import date, timedelta
import importlib.util
import json
from pathlib import Path
import unittest
from unittest import mock
from tempfile import TemporaryDirectory

spec = importlib.util.spec_from_file_location('review_workbench_v2', Path(__file__).resolve().parents[1] / 'scripts/review_workbench_v2.py')
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)
HEAD, MAIN = 'a' * 40, 'b' * 40


def synthetic_template():
    return {'template_id': 'SYNTHETIC', 'version': '1',
            'checks': [{'check_id': f'C{i:02}'} for i in range(1, 11)]}


def bundle(track='original-development'):
    checks = [f'C{i:02}' for i in range(1, 11)]
    return {'format_version': 2, 'kind': 'bundle', 'review_id': 'RV-SYNTHETIC-V2',
            'subject_id': 'SYNTHETIC', 'subject_ref': 'data/reviews/subjects/SYNTHETIC.json',
            'source_revision': 'c' * 40, 'source_repository': 'synthetic/source',
            'source_manifest': [{'path': 'SKILL.md', 'blob_sha': 'd' * 40}], 'track': track,
            'review_scope': ['SKILL.md'], 'excluded_scope': [],
            'template_versions': [{'template_id': 'SYNTHETIC', 'version': '1', 'sha256': w.fingerprint(synthetic_template()),
                                   'template_ref': 'data/reviews/templates/SYNTHETIC.json'}],
            'groups': [{'group_id': 'G1', 'label': 'SYNTHETIC group', 'check_ids': checks}],
            'matrix': [{'file': 'SKILL.md', 'check_id': cid, 'group_id': 'G1',
                        **{key: 'SYNTHETIC not a legal conclusion' for key in
                           ('issue', 'source_locator', 'facts', 'effective_period', 'transitional_rule',
                            'applicability', 'agent_finding', 'risks', 'required_changes', 'limitations')},
                        'authority_refs': ['https://example.invalid/SYNTHETIC'], 'evidence_refs': ['controlled://SYNTHETIC/facts'],
                        'automation_status': 'agent-precheck'} for cid in checks],
            'rights_evidence': {gate: [{'ref': 'controlled://SYNTHETIC/evidence', 'status': 'verified',
                                       'summary': 'SYNTHETIC'}] for gate in w.GATES[track]},
            'validity': {'next_review_date': (date.today() + timedelta(days=30)).isoformat(),
                         'update_triggers': ['source-update', 'regulatory-change', 'license-change']},
            'automation': {'status': 'agent-precheck'}}


def form(b=None, axis='professional_review', decision='approved-scope'):
    b = b or bundle()
    return w.render_form(b, axis).replace('<decision>', decision if axis == 'professional_review' else 'approved-scope', 1).replace(
        'Decision: <decision>', 'Decision: ' + decision).replace('<reason>', 'SYNTHETIC reason').replace(
        '<limitations>', 'SYNTHETIC limitations').replace('<personal declaration>', 'SYNTHETIC COI declaration').replace(
        '<actual YYYY-MM-DD>', date.today().isoformat())


class FakeAPI:
    def __init__(self):
        self.b = bundle()
        self.ledger = None
        self.head = HEAD
        self.policy = {'format_version': 2, 'repository': w.REPOSITORY, 'ci_required': ['SYNTHETIC CI'],
                       'ci_app_id': 15368, 'max_regulatory_age_days': 90,
                       'credential_refs': {'synthetic-human': 'controlled://SYNTHETIC/qualification'}}
        self.roles = {'repository': w.REPOSITORY, 'reviewers': {'synthetic-human': ['Legal Reviewer', 'Human Maintainer']}}
        self.permission = 'write'
        self.events = {1: {'id': 1, 'node_id': 'SYNTHETIC-REVIEW-NODE-1', 'user': {'login': 'synthetic-human', 'type': 'User'}, 'body': form(self.b),
                           'state': 'COMMENTED', 'commit_id': HEAD, 'submitted_at': date.today().isoformat() + 'T00:00:00Z',
                           'html_url': 'https://github.com/fitalex/LexRouter/pull/7#pullrequestreview-1'}}
        self.checks = [{'id': 1, 'name': 'SYNTHETIC CI', 'app': {'id': 15368}, 'head_sha': HEAD,
                        'status': 'completed', 'conclusion': 'success'}]
        self.writes = []
        self.snapshots = {}
        self.mutate_on_review_read = None
        self.review_reads = 0
        self.commits = []
        self.timeline = []
        self.source_tree = {'truncated': False, 'tree': [{'path': 'SKILL.md', 'sha': 'd' * 40, 'type': 'blob', 'mode': '100644'}]}
        self.ci_trees = {}
        self.checks_by_head = {}
        self.pr_state = 'open'
        self.template = synthetic_template()
        self.subject_override = None
        self.graph_queries = []
        self.graph_override = None
        self.last_edited_at = {}

    @staticmethod
    def content(value):
        return {'type': 'file', 'encoding': 'base64', 'content': base64.b64encode(json.dumps(value).encode()).decode()}

    def __call__(self, path, method='GET', payload=None):
        if path == 'graphql':
            assert method == 'POST' and payload['query'] == w.REVIEW_EDIT_QUERY
            self.graph_queries.append(deepcopy(payload))
            if self.graph_override is not None:
                return deepcopy(self.graph_override)
            event = next((e for e in self.events.values() if e.get('node_id') == payload['variables']['node_id']), None)
            if event is None:
                return {'data': {'node': None}}
            return {'data': {'node': {'__typename': 'PullRequestReview', 'id': event['node_id'],
                'databaseId': str(event['id']), 'lastEditedAt': self.last_edited_at.get(event['id']),
                'commit': {'oid': event['commit_id']},
                'pullRequest': {'number': 7, 'repository': {'nameWithOwner': w.REPOSITORY}}}}}
        if path.startswith('repos/synthetic/source/git/trees/'):
            return deepcopy(self.source_tree)
        tail = path.removeprefix(w.PREFIX + '/')
        if tail.startswith('issues/7/timeline?'):
            return deepcopy(self.timeline)
        if tail.startswith('pulls/7/commits?'):
            return deepcopy(self.commits)
        if tail.startswith('git/trees/') and '?recursive=1' in tail:
            ref = tail.split('/')[2].split('?')[0]
            return deepcopy(self.ci_trees.get(ref, {'truncated': False, 'tree': []}))
        if method != 'GET':
            self.writes.append((tail, method, payload))
            if tail == 'git/trees':
                return {'sha': 'e' * 40}
            if tail == 'git/commits':
                return {'sha': 'f' * 40}
            if tail.startswith('git/refs/'):
                if self.head != payload.get('sha') and self.head != HEAD:
                    raise w.ReviewError('SYNTHETIC CAS conflict.')
                return {}
        if tail == 'pulls/7':
            return {'number': 7, 'state': self.pr_state, 'commits': len(self.commits), 'base': {'ref': 'main', 'repo': {'full_name': w.REPOSITORY}},
                    'head': {'sha': self.head, 'ref': 'SYNTHETIC-branch', 'repo': {'full_name': w.REPOSITORY}}}
        if tail.startswith('pulls/7/reviews/'):
            self.review_reads += 1
            if self.mutate_on_review_read:
                self.mutate_on_review_read(self)
            return deepcopy(self.events[int(tail.split('/')[-1])])
        if tail == 'git/ref/heads/main':
            return {'object': {'sha': MAIN}}
        if tail.startswith('collaborators/'):
            return {'permission': self.permission}
        if tail.startswith('compare/'):
            return {'status': 'identical'}
        if tail.startswith('commits/') and '/check-runs?' in tail:
            return {'check_runs': self.checks_by_head.get(tail.split('/')[1], self.checks)}
        if tail.startswith('git/commits/'):
            return {'tree': {'sha': 'c' * 40}}
        if tail.startswith('contents/'):
            name, ref = tail[len('contents/'):].split('?ref=')
            if name == 'data/reviews/templates/SYNTHETIC.json':
                return self.content(self.template)
            if name == 'data/reviews/subjects/SYNTHETIC.json':
                return self.content(self.subject_override or {'subject_id': self.b['subject_id'], 'track': self.b['track'],
                    'source_revision': self.b['source_revision'], 'source_url': 'https://github.com/synthetic/source/blob/ref/SKILL.md',
                    'review_scope': self.b['review_scope'], 'templates': [v['template_ref'] for v in self.b['template_versions']]})
            if name == w.POLICY_PATH:
                return self.content(self.policy)
            if name == 'data/reviews/reviewers.json':
                return self.content(self.roles)
            if (ref, name) in self.snapshots:
                return self.content(self.snapshots[(ref, name)])
            if name.endswith('/bundle.json'):
                return self.content(self.b)
            if name.endswith('/ledger.json') and ref == self.head and self.ledger is not None:
                return self.content(self.ledger)
            raise w.NotFound('SYNTHETIC absent file.')
        raise AssertionError('Unmocked API ' + path)

    def sync(self, **kwargs):
        return w.sync_review(w.REPOSITORY, 7, kwargs.pop('review_number', 1), 'synthetic-human',
                             kwargs.pop('expected_head', self.head), api=self, **kwargs)


class ContractTests(unittest.TestCase):
    def test_full_matrix_and_nonhuman_automation(self):
        b = bundle()
        self.assertEqual(w.validate_bundle(b), b)
        self.assertEqual(w.empty_ledger(b)['entries'], [])
        for mutate in [lambda x: x['matrix'].pop(), lambda x: x['matrix'].append(x['matrix'][0]),
                       lambda x: x['groups'][0]['check_ids'].remove('C01'),
                       lambda x: x['matrix'][0].update(group_id='unknown'),
                       lambda x: x.update(review_scope=['../secret'])]:
            bad = deepcopy(b)
            mutate(bad)
            with self.subTest(mutate=mutate), self.assertRaises(w.ReviewError):
                w.validate_bundle(bad)

    def test_form_has_no_digest_or_url_and_complete_coverage(self):
        parsed = w.parse_form(form())
        self.assertEqual(w.validate_form(parsed, bundle()), parsed)
        self.assertNotIn('digest', parsed)
        for text in [form() + form(), form().replace('COI:', 'Unknown:'),
                     form().replace('Reason: SYNTHETIC reason', 'Reason: <reason>'),
                     form().replace('[findings]', '[findings]\nGroup: G1 | approved-scope | x | y'),
                     form().replace('COI: SYNTHETIC COI declaration', 'COI: x\nCOI: y')]:
            with self.subTest(text=text), self.assertRaises(w.ReviewError):
                w.parse_form(text)
        bad = deepcopy(parsed)
        bad['scope'] = ['other.md']
        with self.assertRaises(w.ReviewError):
            w.validate_form(bad, bundle())

    def test_duplicate_json_and_invalid_schema(self):
        with self.assertRaises(w.ReviewError):
            w.loads('{"x":1,"x":2}')
        with self.assertRaises(w.ReviewError):
            w.loads('{"x":NaN}')
        bad = bundle()
        bad['human_approved'] = True
        with self.assertRaises(w.ReviewError):
            w.validate_bundle(bad)

    def test_actual_date_is_not_future_or_stale(self):
        f = w.parse_form(form())
        for offset in (1, -91):
            f['regulatory_as_of'] = (date.today() + timedelta(days=offset)).isoformat()
            with self.assertRaises(w.ReviewError):
                w.validate_form(f, bundle())


class SyncTests(unittest.TestCase):
    def test_authentic_synthetic_comment_produces_bound_append_only_entry(self):
        api = FakeAPI()
        result = api.sync()
        self.assertEqual(len(result['entries']), 1)
        entry = result['entries'][0]
        self.assertEqual(entry['reviewed_commit_sha'], HEAD)
        self.assertEqual(entry['bundle_sha256'], w.fingerprint(api.b))
        self.assertEqual(entry['event_url'], api.events[1]['html_url'])
        self.assertEqual(api.writes, [])
        w.validate_ledger(result, api.b)
        for field in ('bundle_sha256', 'entry_sha256', 'prior_ledger_sha256'):
            bad = deepcopy(result)
            bad['entries'][0][field] = '0' * 64
            with self.subTest(field=field), self.assertRaises(w.ReviewError):
                w.validate_ledger(bad, api.b)
        with self.assertRaises(w.ReviewError):
            w.validate_ledger(w.empty_ledger(api.b), api.b, result)

    def test_role_permission_qualification_state_and_sender_fail_closed(self):
        mutations = [lambda a: a.roles.update(reviewers={}), lambda a: setattr(a, 'permission', 'read'),
                     lambda a: a.policy.update(credential_refs={}), lambda a: a.events[1].update(state='APPROVED'),
                     lambda a: a.events[1].update(state='DISMISSED'),
                     lambda a: a.events[1]['user'].update(type='Bot'),
                     lambda a: a.events[1]['user'].update(login='someone-else'),
                     lambda a: a.events[1].update(commit_id='f' * 40)]
        for mutate in mutations:
            api = FakeAPI()
            mutate(api)
            with self.subTest(mutate=mutate), self.assertRaises(w.ReviewError):
                api.sync(write=True)
            self.assertEqual(api.writes, [])

    def test_all_three_tracks_require_every_verified_rights_gate(self):
        for track in w.GATES:
            for missing in w.GATES[track]:
                api = FakeAPI()
                api.b = bundle(track)
                del api.b['rights_evidence'][missing]
                with self.subTest(track=track, gate=missing), self.assertRaises(w.ReviewError):
                    api.sync()
            api = FakeAPI()
            api.b = bundle(track)
            api.b['rights_evidence'][next(iter(w.GATES[track]))][0]['status'] = 'not-verified'
            with self.assertRaises(w.ReviewError):
                api.sync()

    def test_ci_missing_failed_stale_wrong_app_and_latest_rerun_block(self):
        mutations = [lambda a: a.checks.clear(), lambda a: a.checks[0].update(conclusion='failure'),
                     lambda a: a.checks[0].update(head_sha='f' * 40),
                     lambda a: a.checks[0]['app'].update(id=1),
                     lambda a: a.checks.append({**a.checks[0], 'id': 2, 'status': 'queued'})]
        for mutate in mutations:
            api = FakeAPI()
            mutate(api)
            with self.subTest(mutate=mutate), self.assertRaises(w.ReviewError):
                api.sync()

    def test_expired_review_and_unresolved_group_block(self):
        api = FakeAPI()
        api.b['validity']['next_review_date'] = date.today().isoformat()
        with self.assertRaises(w.ReviewError):
            api.sync()
        api = FakeAPI()
        api.events[1]['body'] = form().replace('G1 | approved-scope', 'G1 | needs-changes')
        with self.assertRaises(w.ReviewError):
            api.sync()

    def test_independent_maintainer_event_required(self):
        api = FakeAPI()
        api.events[1]['body'] = form(axis='admission_decision', decision='admitted')
        with self.assertRaises(w.ReviewError):
            api.sync()

    def test_needs_changes_can_be_recorded_without_claiming_passed_gates(self):
        api = FakeAPI()
        api.events[1]['body'] = form(decision='needs-changes')
        api.checks = []
        result = api.sync()
        self.assertEqual(result['entries'][0]['form']['decision'], 'needs-changes')

    def test_edited_dismissed_and_concurrent_events_make_no_writes(self):
        for action in ('edited', 'dismissed'):
            api = FakeAPI()
            with self.assertRaises(w.ReviewError):
                api.sync(event_action=action, write=True)
            self.assertEqual(api.writes, [])
        api = FakeAPI()
        def mutate(a):
            if a.review_reads >= 2:
                a.events[1]['body'] += '\nSYNTHETIC edited'
        api.mutate_on_review_read = mutate
        with self.assertRaises(w.ReviewError):
            api.sync(write=True)
        self.assertEqual(api.writes, [])

    def test_cas_changes_only_ledger_and_never_force_pushes(self):
        api = FakeAPI()
        api.sync(write=True)
        self.assertEqual(len(api.writes), 3)
        tree = api.writes[0][2]['tree']
        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0]['path'], w.review_path(api.b['review_id'], 'ledger'))
        self.assertEqual(api.writes[1][2]['parents'], [HEAD])
        self.assertIs(api.writes[-1][2]['force'], False)

    def test_historical_event_edit_revoke_and_bundle_change_are_blocked(self):
        for change in ('edit', 'dismiss', 'permission', 'bundle', 'prior'):
            api = FakeAPI()
            ledger = api.sync()
            api.ledger = ledger
            api.snapshots[(HEAD, w.review_path(api.b['review_id'], 'ledger'))] = w.empty_ledger(api.b)
            api.head = 'e' * 40
            if change == 'edit':
                api.events[1]['body'] += '\nSYNTHETIC changed'
            elif change == 'dismiss':
                api.events[1]['state'] = 'DISMISSED'
            elif change == 'permission':
                api.permission = 'read'
            elif change == 'bundle':
                api.b['matrix'][0]['agent_finding'] = 'SYNTHETIC altered'
            elif change == 'prior':
                api.snapshots[(HEAD, w.review_path(api.b['review_id'], 'ledger'))] = ledger
            with self.subTest(change=change), self.assertRaises(w.ReviewError):
                w.online_validate(w.REPOSITORY, 7, api.b['review_id'], api)

    def test_two_events_preserve_history_and_allow_same_dual_role_human(self):
        api = FakeAPI()
        first = api.sync()
        api.ledger = first
        api.snapshots[(HEAD, w.review_path(api.b['review_id'], 'ledger'))] = w.empty_ledger(api.b)
        api.head = 'e' * 40
        api.checks_by_head[HEAD] = deepcopy(api.checks)
        api.checks[0]['head_sha'] = api.head
        api.events[2] = {**api.events[1], 'id': 2, 'node_id': 'SYNTHETIC-REVIEW-NODE-2', 'commit_id': api.head,
                         'body': form(axis='admission_decision', decision='admitted'),
                         'html_url': 'https://github.com/fitalex/LexRouter/pull/7#pullrequestreview-2'}
        result = api.sync(review_number=2)
        self.assertEqual(result['entries'][0], first['entries'][0])
        self.assertEqual(result['entries'][1]['form']['decision'], 'admitted')
        self.assertNotEqual(result['entries'][0]['event_id'], result['entries'][1]['event_id'])


class SecurityRegressionTests(unittest.TestCase):
    def signed_fixture(self):
        api = FakeAPI()
        result = api.sync()
        api.ledger = result
        api.snapshots[(HEAD, w.review_path(api.b['review_id'], 'ledger'))] = w.empty_ledger(api.b)
        api.head = 'e' * 40
        return api, result

    def test_edit_before_first_import_is_rejected_without_writes(self):
        api = FakeAPI()
        api.last_edited_at[1] = date.today().isoformat() + 'T00:01:00Z'
        with self.assertRaisesRegex(w.ReviewError, 'Edited Reviews'):
            api.sync(write=True)
        self.assertEqual(api.writes, [])
        self.assertEqual(len(api.graph_queries), 1)

    def test_graphql_identity_missing_fields_and_partial_errors_fail_closed(self):
        good = {'__typename': 'PullRequestReview', 'id': 'SYNTHETIC-REVIEW-NODE-1', 'databaseId': '1',
                'lastEditedAt': None, 'commit': {'oid': HEAD},
                'pullRequest': {'number': 7, 'repository': {'nameWithOwner': w.REPOSITORY}}}
        mutations = [lambda n: n.update(__typename='IssueComment'), lambda n: n.update(id='different-node'),
                     lambda n: n.update(databaseId='2'), lambda n: n['commit'].update(oid='0' * 40),
                     lambda n: n['pullRequest'].update(number=8),
                     lambda n: n['pullRequest']['repository'].update(nameWithOwner='synthetic/other'),
                     lambda n: n.pop('lastEditedAt')]
        for mutate in mutations:
            api = FakeAPI()
            node = deepcopy(good)
            mutate(node)
            api.graph_override = {'data': {'node': node}}
            with self.subTest(mutate=mutate), self.assertRaises(w.ReviewError):
                api.sync(write=True)
            self.assertEqual(api.writes, [])
        for response in ({'data': {'node': None}}, {'data': {'node': good}, 'errors': [{'message': 'SYNTHETIC error'}]}, {}):
            api = FakeAPI()
            api.graph_override = response
            with self.subTest(response=response), self.assertRaises(w.ReviewError):
                api.sync(write=True)
            self.assertEqual(api.writes, [])
        api = FakeAPI()
        del api.events[1]['node_id']
        with self.assertRaises(w.ReviewError):
            api.sync(write=True)
        self.assertEqual(api.writes, [])

    def test_edit_after_initial_read_is_rechecked_before_writing(self):
        api = FakeAPI()
        def mutate(a):
            if a.review_reads >= 2:
                a.last_edited_at[1] = date.today().isoformat() + 'T00:01:00Z'
        api.mutate_on_review_read = mutate
        with self.assertRaisesRegex(w.ReviewError, 'Edited Reviews'):
            api.sync(write=True)
        self.assertEqual(api.writes, [])
        self.assertGreaterEqual(len(api.graph_queries), 2)

    def test_graphql_adapter_only_allows_the_fixed_read_query(self):
        good = {'query': w.REVIEW_EDIT_QUERY, 'variables': {'node_id': 'SYNTHETIC-NODE'}}
        response = mock.Mock(returncode=0, stdout='{"data":{"node":null}}')
        with mock.patch.object(w.subprocess, 'run', return_value=response) as run:
            self.assertEqual(w.github_api('graphql', 'POST', good), {'data': {'node': None}})
            run.assert_called_once()
        bad_payloads = [{'query': 'mutation { dangerous }', 'variables': {'node_id': 'SYNTHETIC'}},
                        {'query': w.REVIEW_EDIT_QUERY, 'variables': {'node_id': 'SYNTHETIC', 'extra': 1}},
                        {'query': w.REVIEW_EDIT_QUERY, 'variables': {'node_id': ''}},
                        {**good, 'operationName': 'SomethingElse'}]
        with mock.patch.object(w.subprocess, 'run') as run:
            for payload in bad_payloads:
                with self.subTest(payload=payload), self.assertRaises(w.ReviewError):
                    w.github_api('graphql', 'POST', payload)
            with self.assertRaises(w.ReviewError):
                w.github_api('graphql', 'GET', good)
            run.assert_not_called()

    def test_unverified_date_allowed_only_for_nonapproval(self):
        for decision in ('needs-changes', 'rejected', 'approved-scope'):
            api = FakeAPI()
            api.events[1]['body'] = form(decision=decision).replace(date.today().isoformat(), 'not-verified')
            if decision == 'approved-scope':
                with self.assertRaises(w.ReviewError):
                    api.sync()
            else:
                self.assertEqual(api.sync()['entries'][0]['form']['regulatory_as_of'], 'not-verified')
        with self.assertRaises(w.ReviewError):
            w.parse_form(form().replace('SYNTHETIC COI declaration', '〈本人填写〉'))

    def test_fake_admitted_ledger_must_replay_missing_professional_gate(self):
        api = FakeAPI()
        api.events[1]['body'] = form(axis='admission_decision', decision='admitted')
        trusted = {'roles': api.roles, 'policy': api.policy}
        forged = w.append_event(api.b, w.empty_ledger(api.b), api.events[1],
                                w.parse_form(api.events[1]['body']), 'synthetic-human', 7, MAIN, trusted)
        api.snapshots[(HEAD, w.review_path(api.b['review_id'], 'ledger'))] = w.empty_ledger(api.b)
        with self.assertRaisesRegex(w.ReviewError, 'professional'):
            w.verify_saved_history(api.b, forged, api)

    def test_replayed_history_rechecks_ci_and_mirrored_event_metadata(self):
        for variant in ('ci', 'time', 'url'):
            api, ledger = self.signed_fixture()
            if variant == 'ci':
                api.checks[0]['conclusion'] = 'failure'
            else:
                field = 'submitted_at' if variant == 'time' else 'event_url'
                ledger['entries'][0][field] = ('2000-01-01T00:00:00Z' if variant == 'time'
                                                else 'https://example.invalid/SYNTHETIC')
                entry = ledger['entries'][0]
                entry['entry_sha256'] = w.fingerprint({k: v for k, v in entry.items() if k != 'entry_sha256'})
            with self.subTest(variant=variant), self.assertRaises(w.ReviewError):
                w.verify_saved_history(api.b, ledger, api)

    def test_deleted_unmerged_ledger_and_force_push_block(self):
        for variant in ('deleted', 'force-push', 'too-long', 'truncated'):
            api, ledger = self.signed_fixture()
            api.commits = [{'sha': 'f' * 40}]
            api.snapshots[('f' * 40, w.review_path(api.b['review_id'], 'ledger'))] = ledger
            if variant == 'deleted':
                api.ledger = w.empty_ledger(api.b)
            elif variant == 'force-push':
                api.timeline = [{'event': 'head_ref_force_pushed'}]
            elif variant == 'too-long':
                api.commits = [{'sha': 'f' * 40}] * 251
            else:
                original = api.__call__
                def truncated(path, method='GET', payload=None):
                    if '/commits?per_page' in path:
                        return []
                    return original(path, method, payload)
                with self.assertRaises(w.ReviewError):
                    w.immutable_history(truncated, 7, api.b, ledger)
                continue
            with self.subTest(variant=variant), self.assertRaises(w.ReviewError):
                w.online_validate(w.REPOSITORY, 7, api.b['review_id'], api)

    def test_main_subject_template_and_full_source_inventory_anchors(self):
        for variant in ('subject', 'template', 'blob', 'omitted-file', 'truncated-source'):
            api = FakeAPI()
            if variant == 'subject':
                api.subject_override = {'subject_id': 'SYNTHETIC', 'templates': ['missing-specialized']}
            elif variant == 'template':
                api.template['checks'].append({'check_id': 'SPECIAL01'})
            elif variant == 'blob':
                api.source_tree['tree'][0]['sha'] = '0' * 40
            elif variant == 'omitted-file':
                api.source_tree['tree'].append({'path': 'omitted.md', 'sha': '1' * 40, 'type': 'blob', 'mode': '100644'})
            else:
                api.source_tree['truncated'] = True
            with self.subTest(variant=variant), self.assertRaises(w.ReviewError):
                api.sync()

    def test_ci_execution_closure_rejects_import_hooks_workflows_and_executables(self):
        for path in ('json.py', 'sitecustomize.py', '.github/workflows/validate-skills.yml',
                     'scripts/review_workbench_v2.py', 'data/reviews/v2/RV-SYNTHETIC-V2/evil.py'):
            api = FakeAPI()
            api.ci_trees[HEAD] = {'truncated': False, 'tree': [{'path': path, 'sha': 'f' * 40,
                                                              'mode': '100644', 'type': 'blob'}]}
            with self.subTest(path=path), self.assertRaises(w.ReviewError):
                api.sync()
        api = FakeAPI()
        api.ci_trees[HEAD] = {'truncated': False, 'tree': [{'path': 'data/reviews/cases/RV-SYNTHETIC/human-review.md',
                                                          'sha': 'f' * 40, 'mode': '100644', 'type': 'blob'}]}
        self.assertEqual(len(api.sync()['entries']), 1)

    def test_no_legal_evidence_or_unverified_applicability_blocks_approval(self):
        for field, value in (('authority_refs', []), ('evidence_refs', []),
                             ('effective_period', 'not-verified'), ('applicability', '待核')):
            api = FakeAPI()
            api.b['matrix'][0][field] = value
            with self.subTest(field=field), self.assertRaises(w.ReviewError):
                api.sync()

    def test_closed_original_pr_history_remains_auditable(self):
        api, ledger = self.signed_fixture()
        api.pr_state = 'closed'
        self.assertEqual(w.verify_saved_history(api.b, ledger, api), ledger)
        with self.assertRaises(w.ReviewError):
            w.online_validate(w.REPOSITORY, 7, api.b['review_id'], api)

    def test_historical_expiry_is_not_renewal_and_does_not_deadlock_new_reviews(self):
        api = FakeAPI()
        past = date.today() - timedelta(days=150)
        api.b['validity']['next_review_date'] = (past + timedelta(days=30)).isoformat()
        api.events[1]['body'] = form(api.b).replace(date.today().isoformat(), past.isoformat())
        api.events[1]['submitted_at'] = past.isoformat() + 'T00:00:00Z'
        trusted = {'roles': api.roles, 'policy': api.policy}
        ledger = w.append_event(api.b, w.empty_ledger(api.b), api.events[1],
                                w.parse_form(api.events[1]['body']), 'synthetic-human', 7, MAIN, trusted)
        api.snapshots[(HEAD, w.review_path(api.b['review_id'], 'ledger'))] = w.empty_ledger(api.b)
        api.permission = 'read'
        api.pr_state = 'closed'
        self.assertEqual(w.verify_saved_history(api.b, ledger, api), ledger)
        with self.assertRaises(w.ReviewError):
            w.verify_saved_history(api.b, ledger, api, active=True)

    def test_terminal_events_cannot_be_replayed_or_replaced(self):
        api, ledger = self.signed_fixture()
        trusted = {'roles': api.roles, 'policy': api.policy}
        with self.assertRaises(w.ReviewError):
            w.append_event(api.b, ledger, api.events[1], w.parse_form(api.events[1]['body']),
                           'synthetic-human', 7, MAIN, trusted)
        event = {**api.events[1], 'id': 2}
        with self.assertRaises(w.ReviewError):
            w.append_event(api.b, ledger, event, w.parse_form(event['body']), 'synthetic-human', 7, MAIN, trusted)

    def test_local_empty_and_unsigned_data_need_no_online_identity(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(w.validate_local(root, online=True, api=lambda *_: self.fail('Unexpected online lookup')), 0)
            path = root / w.review_path('RV-SYNTHETIC-V2', 'bundle')
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(bundle()))
            self.assertEqual(w.validate_local(root, online=True, api=lambda *_: self.fail('Unexpected online lookup')), 1)
            path.with_name('ledger.json').write_text(json.dumps(w.empty_ledger(bundle())))
            self.assertEqual(w.validate_local(root, online=True, api=lambda *_: self.fail('Unexpected online lookup')), 1)
            path.unlink()
            with self.assertRaises(w.ReviewError):
                w.validate_local(root)

    def test_local_baseline_rejects_deleted_signed_history(self):
        api = FakeAPI()
        ledger = api.sync()
        ledger_path = w.review_path(api.b['review_id'], 'ledger')
        def git(root, args):
            if args[0] == 'rev-parse':
                return MAIN
            if args[0] == 'ls-tree':
                return ledger_path
            return json.dumps(ledger)
        with TemporaryDirectory() as directory, mock.patch.object(w, 'git_output', side_effect=git):
            with self.assertRaisesRegex(w.ReviewError, 'deleted'):
                w.validate_local(Path(directory), base_ref='origin/main')

    def test_public_tripwire_rejects_obvious_private_material(self):
        b = bundle()
        b['matrix'][0]['facts'] = 'PRIVATE_MATERIAL'
        with self.assertRaises(w.ReviewError):
            w.validate_bundle(b)


if __name__ == '__main__':
    unittest.main()
