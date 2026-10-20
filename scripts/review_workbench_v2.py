#!/usr/bin/env python3
"""Independent v2 contract and trusted GitHub Review importer; never execute PR code.

Only this module/schema from an accepted main checkout may run with write access.
All JSON, review text and git contents retrieved from a PR are untrusted data.
"""
import argparse
import base64
from copy import deepcopy
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'fitalex/LexRouter'
PREFIX = 'repos/' + REPOSITORY
POLICY_PATH = 'data/reviews/workbench-v2-policy.json'
# A fixed read-only query is the sole permitted operation at /graphql. The alias
# preserves a stable response key while avoiding deprecated 32-bit databaseId.
REVIEW_EDIT_QUERY = """query LexRouterReviewEditState($node_id: ID!) {
  node(id: $node_id) {
    __typename
    ... on PullRequestReview {
      id
      databaseId: fullDatabaseId
      lastEditedAt
      commit { oid }
      pullRequest { number repository { nameWithOwner } }
    }
  }
}"""
ROLES = {'professional_review': 'Legal Reviewer', 'admission_decision': 'Human Maintainer'}
GATES = {
    'curated-hosting': ('authorization-chain', 'hosting-scope', 'attribution-and-notices'),
    'original-development': ('independent-requirements', 'original-design', 'provenance-and-dependencies', 'synthetic-tests'),
    'external-reference': ('index-description', 'no-fulltext-copy', 'metadata-and-dedup'),
}
V2_DIRECTORY = 'data/reviews/v2'
RID = re.compile(r'RV-[A-Za-z0-9-]+\Z')
SHA = re.compile(r'[a-f0-9]{40}\Z')


class ReviewError(ValueError):
    """Fixed diagnostics intentionally exclude untrusted review contents."""


class NotFound(ReviewError):
    pass


def require(condition, message):
    if not condition:
        raise ReviewError(message)


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def loads(content):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON keys are forbidden.')
            result[key] = value
        return result
    try:
        return json.loads(content, object_pairs_hook=unique,
                          parse_constant=lambda _: (_ for _ in ()).throw(ReviewError('Non-finite JSON is forbidden.')))
    except (ValueError, TypeError, UnicodeError):
        raise ReviewError('Invalid JSON; contents were not logged.') from None


def public_guard(value):
    text = json.dumps(value, ensure_ascii=False)
    patterns = (r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY', r'AKIA[A-Z0-9]{16}',
                r'(?<![A-Za-z0-9])\d{17}[0-9Xx](?![A-Za-z0-9])',
                r'(?i)\b(?:secret|token|password)\s*[=:]\s*[^\s,;]+',
                r'(?i)(?:file://|/home/|/Users/)', r'(?i)PRIVATE_MATERIAL')
    require(not any(re.search(pattern, text) for pattern in patterns),
            'Public-material safety tripwire failed; inspect privately. Input was not logged.')


def schema_check(value, kind):
    public_guard(value)
    schema = loads((ROOT / 'schemas/review-record-v2.schema.json').read_text())
    validator = Draft202012Validator({'$ref': '#/$defs/' + kind, '$defs': schema['$defs']},
                                    format_checker=FormatChecker())
    require(not list(validator.iter_errors(value)), 'V2 contract validation failed.')


def safe_path(path):
    require(isinstance(path, str) and path and not path.startswith('/') and '\\' not in path
            and all(p not in ('', '.', '..') for p in path.split('/')),
            'Expected an explicit safe repository-relative file path.')
    return path


def reference(value):
    require(isinstance(value, str) and bool(re.fullmatch(r'(?:controlled://[A-Za-z0-9_./-]+|https://[^\s?@]+)', value)),
            'Evidence requires a public HTTPS locator or controlled index.')


def validate_bundle(bundle):
    schema_check(bundle, 'bundle')
    scope = bundle['review_scope']
    require(len(scope) == len(set(scope)), 'Duplicate scope files.')
    require(len(bundle['excluded_scope']) == len(set(bundle['excluded_scope'])), 'Duplicate exclusions.')
    require(not set(scope) & set(bundle['excluded_scope']), 'Selected and excluded scopes overlap.')
    manifest = {f['path']: f['blob_sha'] for f in bundle['source_manifest']}
    require(len(manifest) == len(bundle['source_manifest']) and set(manifest) == set(scope),
            'Source manifest must pin every selected file exactly once.')
    for path in scope + bundle['excluded_scope']:
        safe_path(path)
    groups, checks = {}, {}
    for group in bundle['groups']:
        gid = group['group_id']
        require(gid not in groups, 'Duplicate group ID.')
        groups[gid] = group
        for cid in group['check_ids']:
            require(cid not in checks, 'Each check must map to exactly one group.')
            checks[cid] = gid
    require({f'C{i:02}' for i in range(1, 11)} <= checks.keys(), 'C01-C10 coverage is mandatory.')
    seen = set()
    for row in bundle['matrix']:
        pair = (row['file'], row['check_id'])
        require(pair not in seen and row['file'] in scope and checks.get(row['check_id']) == row['group_id'],
                'Invalid or duplicate file/check/group mapping.')
        seen.add(pair)
        for ref in row['authority_refs'] + row['evidence_refs']:
            reference(ref)
    require(seen == {(path, cid) for path in scope for cid in checks}, 'Full per-file matrix coverage is mandatory.')
    for evidence in bundle['rights_evidence'].values():
        for item in evidence:
            reference(item['ref'])
    require(len({v['template_id'] for v in bundle['template_versions']}) == len(bundle['template_versions']),
            'Duplicate template version.')
    return bundle


def parse_form(body):
    """A small plain-text form: no YAML evaluation, JSON editing or digest copying."""
    blocks = re.findall(r'^```lexrouter-review-v2\s*\n(.*?)^```\s*$', body or '', flags=re.M | re.S)
    require(len(blocks) == 1, 'Exactly one v2 short-form block is required.')
    sections = {'scope': {'Review-ID', 'Scope'}, 'findings': {'Group'},
                'professional_decision': {'Axis', 'Decision', 'Reason', 'Limitations', 'COI'},
                'maintenance': {'Regulatory-As-Of'}}
    section, visited, fields, paths, groups = None, set(), {}, [], []
    for raw in blocks[0].splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith('[') and line.endswith(']'):
            section = line[1:-1]
            require(section in sections and section not in visited, 'Unknown or duplicate short-form section.')
            visited.add(section)
            continue
        require(section is not None and ': ' in line, 'Invalid short-form field syntax.')
        key, value = line.split(': ', 1)
        value = value.strip()
        require(key in sections[section] and value and not any(mark in value for mark in ('<', '>', '〈', '〉')),
                'Missing, placeholder or unknown short-form field.')
        if key == 'Scope':
            paths.append(value)
        elif key == 'Group':
            parts = [part.strip() for part in value.split('|')]
            require(len(parts) == 4 and all(parts), 'Group requires ID, decision, reason and limitations.')
            groups.append(dict(zip(('group_id', 'decision', 'reason', 'limitations'), parts)))
        else:
            require(key not in fields, 'Duplicate short-form field.')
            fields[key] = value
    require(visited == set(sections), 'All four short-form sections are required.')
    names = {'Review-ID': 'review_id', 'Axis': 'axis', 'Decision': 'decision', 'Reason': 'reason',
             'Limitations': 'limitations', 'COI': 'conflict_declaration', 'Regulatory-As-Of': 'regulatory_as_of'}
    form = {names[k]: v for k, v in fields.items()}
    form.update(scope=paths, groups=groups)
    schema_check(form, 'form')
    require(len(paths) == len(set(paths)) and len(groups) == len({g['group_id'] for g in groups}),
            'Duplicate scope or group decision.')
    return form


def render_form(bundle, axis='professional_review'):
    validate_bundle(bundle)
    require(axis in ROLES, 'Unknown human decision axis.')
    return '\n'.join(['```lexrouter-review-v2', '[scope]', 'Review-ID: ' + bundle['review_id'],
        *['Scope: ' + path for path in bundle['review_scope']], '[findings]',
        *['Group: ' + g['group_id'] + ' | <decision> | <reason> | <limitations>' for g in bundle['groups']],
        '[professional_decision]', 'Axis: ' + axis, 'Decision: <decision>', 'Reason: <reason>',
        'Limitations: <limitations>', 'COI: <personal declaration>', '[maintenance]',
        'Regulatory-As-Of: <actual YYYY-MM-DD>', '```', ''])


def validate_form(form, bundle, today=None, max_age=90):
    schema_check(form, 'form')
    require(form['review_id'] == bundle['review_id'] and set(form['scope']) == set(bundle['review_scope']),
            'Short form must identify the entire exact review scope.')
    require(len(form['scope']) == len(set(form['scope'])), 'Duplicate scope.')
    require({g['group_id'] for g in form['groups']} == {g['group_id'] for g in bundle['groups']}
            and len(form['groups']) == len(bundle['groups']), 'Short form must decide every group exactly once.')
    decisions = ('approved-scope', 'needs-changes', 'rejected') if form['axis'] == 'professional_review' else ('admitted', 'declined', 'suspended')
    require(form['decision'] in decisions, 'Decision is not valid for this human axis.')
    if form['decision'] in ('approved-scope', 'admitted'):
        require(all(g['decision'] in ('approved-scope', 'not-applicable') for g in form['groups']),
                'Unresolved group decisions block approval.')
        require(form['regulatory_as_of'] != 'not-verified', 'Approval requires an actual legal verification date.')
        actual = date.fromisoformat(form['regulatory_as_of'])
        age = ((today or datetime.now(timezone.utc).date()) - actual).days
        require(0 <= age <= max_age, 'Actual legal verification date is future or stale.')
    return form


def empty_ledger(bundle):
    return {'format_version': 2, 'kind': 'ledger', 'review_id': bundle['review_id'],
            'bundle_sha256': fingerprint(bundle), 'entries': []}


def validate_ledger(ledger, bundle, baseline=None):
    schema_check(ledger, 'ledger')
    require(ledger['review_id'] == bundle['review_id'] and ledger['bundle_sha256'] == fingerprint(bundle),
            'Signed bundle changed; create a new Review ID.')
    prior, event_ids = None, set()
    for i, entry in enumerate(ledger['entries']):
        content = {k: v for k, v in entry.items() if k != 'entry_sha256'}
        prefix = {**ledger, 'entries': ledger['entries'][:i]}
        require(entry['sequence'] == i + 1 and entry['previous_sha256'] == prior
                and fingerprint(content) == entry['entry_sha256']
                and entry['prior_ledger_sha256'] == fingerprint(prefix)
                and entry['bundle_sha256'] == ledger['bundle_sha256'], 'Ledger hash chain is invalid.')
        require(entry['event_id'] not in event_ids, 'A GitHub event cannot be replayed across decisions.')
        event_ids.add(entry['event_id'])
        validate_form(entry['form'], bundle, today=date.fromisoformat(entry['submitted_at'][:10]), max_age=36600)
        prior = entry['entry_sha256']
    if baseline:
        validate_ledger(baseline, bundle)
        require(ledger['entries'][:len(baseline['entries'])] == baseline['entries'], 'Accepted ledger history is append-only.')
    return ledger


def github_api(path, method='GET', payload=None):
    fixed_graphql = (path == 'graphql' and method == 'POST' and isinstance(payload, dict)
                     and set(payload) == {'query', 'variables'} and payload['query'] == REVIEW_EDIT_QUERY
                     and isinstance(payload['variables'], dict) and set(payload['variables']) == {'node_id'}
                     and isinstance(payload['variables']['node_id'], str)
                     and 0 < len(payload['variables']['node_id']) <= 1024)
    require(fixed_graphql or path.startswith(PREFIX + '/') or (method == 'GET' and re.fullmatch(
        r'repos/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/git/trees/[a-f0-9]{40}\?recursive=1', path)),
        'Only configured repository operations, immutable source-tree reads and the fixed Review edit query are allowed.')
    command = ['gh', 'api', '--method', method, path]
    if payload is not None:
        command += ['--input', '-']
    try:
        result = subprocess.run(command, input=json.dumps(payload) if payload is not None else None,
                                capture_output=True, text=True, timeout=60, check=False)
    except (OSError, subprocess.SubprocessError):
        raise ReviewError('GitHub API unavailable; no decision was imported.') from None
    if result.returncode:
        if method == 'GET' and 'HTTP 404' in result.stderr:
            raise NotFound('GitHub resource is absent.')
        raise ReviewError('GitHub API failed; no decision was imported.')
    return loads(result.stdout) if result.stdout.strip() else {}


def content_at(api, path, ref, optional=False):
    safe_path(path)
    require(SHA.fullmatch(ref), 'Content must be read at an immutable Git commit.')
    try:
        value = api(f'{PREFIX}/contents/{quote(path, safe="/")}?ref={ref}')
    except NotFound:
        if optional:
            return None
        raise
    require(isinstance(value, dict) and value.get('type') == 'file' and value.get('encoding') == 'base64',
            'Expected a regular base64-encoded repository file.')
    try:
        raw = base64.b64decode(value['content'], validate=False)
        require(len(raw) <= 4_000_000, 'Review data exceeds the supported size.')
        return loads(raw)
    except (KeyError, ValueError):
        raise ReviewError('Repository snapshot could not be decoded.') from None


def policy_at(api, main_sha):
    roles = content_at(api, 'data/reviews/reviewers.json', main_sha)
    policy = content_at(api, POLICY_PATH, main_sha)
    require(roles.get('repository') == REPOSITORY and policy.get('repository') == REPOSITORY
            and policy.get('format_version') == 2, 'Trusted main reviewer policy is invalid.')
    require(isinstance(policy.get('ci_required'), list) and policy['ci_required']
            and all(isinstance(n, str) and n for n in policy['ci_required'])
            and policy.get('ci_app_id') == 15368, 'Trusted main CI policy is missing.')
    require(type(policy.get('max_regulatory_age_days')) is int
            and 1 <= policy['max_regulatory_age_days'] <= 366, 'Trusted main freshness policy is invalid.')
    return {'roles': roles, 'policy': policy}


def main_sha(api):
    sha = api(f'{PREFIX}/git/ref/heads/main')['object']['sha']
    require(SHA.fullmatch(sha), 'Trusted main reference unavailable.')
    return sha


def pull(api, number):
    pr = api(f'{PREFIX}/pulls/{number}')
    require(pr.get('number') == number and pr.get('state') == 'open'
            and pr.get('base', {}).get('ref') == 'main'
            and pr.get('base', {}).get('repo', {}).get('full_name') == REPOSITORY
            and pr.get('head', {}).get('repo', {}).get('full_name') == REPOSITORY
            and pr['head'].get('ref') != 'main' and SHA.fullmatch(pr['head'].get('sha', '')),
            'Only an open same-repository PR targeting main is supported.')
    return pr


def event_snapshot(event):
    result = {key: event.get(key) for key in ('id', 'node_id', 'body', 'state', 'commit_id', 'submitted_at', 'html_url')}
    result['user'] = {key: event.get('user', {}).get(key) for key in ('id', 'login', 'type')}
    return result


def verify_unedited_review(api, number, event):
    """REST exposes no edit time; read it independently from the bound review node."""
    node_id = event.get('node_id')
    require(isinstance(node_id, str) and 0 < len(node_id) <= 1024,
            'Review node identity is unavailable; edit history cannot be verified.')
    result = api('graphql', method='POST', payload={
        'query': REVIEW_EDIT_QUERY, 'variables': {'node_id': node_id}})
    require(isinstance(result, dict) and not result.get('errors')
            and isinstance(result.get('data'), dict), 'Review edit-history lookup failed.')
    node = result['data'].get('node')
    require(isinstance(node, dict) and node.get('__typename') == 'PullRequestReview'
            and node.get('id') == node_id and type(event.get('id')) is int
            and isinstance(node.get('databaseId'), (int, str))
            and str(node['databaseId']) == str(event['id'])
            and isinstance(node.get('commit'), dict) and node['commit'].get('oid') == event.get('commit_id')
            and isinstance(node.get('pullRequest'), dict) and node['pullRequest'].get('number') == number
            and isinstance(node['pullRequest'].get('repository'), dict)
            and node['pullRequest']['repository'].get('nameWithOwner') == REPOSITORY,
            'GraphQL Review identity does not match the REST event, commit and repository PR.')
    require('lastEditedAt' in node and node['lastEditedAt'] is None,
            'Edited Reviews cannot be imported or retained as signed approval; submit a new Comment Review.')


def authenticate(api, number, event, actor, trusted, expected_head=None, current_permissions=True):
    user = event.get('user', {})
    require(event.get('state') == 'COMMENTED' and event.get('submitted_at')
            and user.get('type') == 'User' and user.get('login') == actor
            and not actor.endswith('[bot]') and SHA.fullmatch(event.get('commit_id', '')),
            'Only the human author’s submitted Comment Review is a signature.')
    require(event.get('html_url') == f'https://github.com/{REPOSITORY}/pull/{number}#pullrequestreview-{event.get("id")}',
            'Review event does not belong to this PR.')
    if expected_head:
        require(event['commit_id'] == expected_head, 'Review event does not reference the current PR head.')
    verify_unedited_review(api, number, event)
    form = parse_form(event.get('body', ''))
    require(ROLES[form['axis']] in trusted['roles'].get('reviewers', {}).get(actor, []),
            'Actor lacks the human role in accepted main policy.')
    credential = trusted['policy'].get('credential_refs', {}).get(actor)
    require(isinstance(credential, str) and credential.startswith('controlled://'),
            'Accepted one-time reviewer qualification index is missing.')
    reference(credential)
    if current_permissions:
        permission = api(f'{PREFIX}/collaborators/{quote(actor, safe="")}/permission')
        require(permission.get('permission') in ('write', 'maintain', 'admin'), 'Actor lacks current repository write permission.')
    return form


def ensure_gates(api, bundle, form, ledger, head, trusted, today=None):
    today = today or datetime.now(timezone.utc).date()
    validate_form(form, bundle, today=today, max_age=trusted['policy']['max_regulatory_age_days'])
    if form['decision'] not in ('approved-scope', 'admitted'):
        return
    require(date.fromisoformat(bundle['validity']['next_review_date']) > today,
            'Next legal review date is absent or overdue.')
    require(set(bundle['rights_evidence']) == set(GATES[bundle['track']]), 'Track-specific rights evidence is incomplete.')
    for gate in GATES[bundle['track']]:
        require(bundle['rights_evidence'][gate] and all(x['status'] == 'verified' for x in bundle['rights_evidence'][gate]),
                'Unverified track-specific rights evidence blocks approval.')
    accepted = {g['group_id'] for g in form['groups'] if g['decision'] == 'approved-scope'}
    for row in bundle['matrix']:
        if row['group_id'] in accepted:
            require(row['authority_refs'] and row['evidence_refs']
                    and all(not any(mark in row[key].lower() for mark in ('not-verified', '待核', '未核', '〈', '<'))
                            for key in ('facts', 'effective_period', 'transitional_rule', 'applicability')),
                    'Accepted legal findings require actual authorities, factual evidence and resolved applicability/timing.')
    checks = []
    page = 1
    while True:
        response = api(f'{PREFIX}/commits/{head}/check-runs?per_page=100&page={page}')
        batch = response.get('check_runs', [])
        checks.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        require(page <= 100, 'CI evidence pagination limit exceeded.')
    for name in trusted['policy']['ci_required']:
        matches = [c for c in checks if c.get('name') == name and c.get('app', {}).get('id') == 15368]
        require(matches, 'Required trusted GitHub Actions check is missing.')
        latest = max(matches, key=lambda x: x.get('id', 0))
        require(latest.get('head_sha') == head and latest.get('status') == 'completed'
                and latest.get('conclusion') == 'success', 'Required current-head CI check did not succeed.')
    if form['axis'] == 'admission_decision':
        professional = [e for e in ledger['entries'] if e['form']['axis'] == 'professional_review']
        require(professional and professional[-1]['form']['decision'] == 'approved-scope',
                'Independent professional approval must precede admission.')
        validate_form(professional[-1]['form'], bundle, today=today, max_age=trusted['policy']['max_regulatory_age_days'])


def review_path(rid, name):
    require(isinstance(rid, str) and RID.fullmatch(rid), 'Invalid v2 Review ID.')
    return f'data/reviews/v2/{rid}/{name}.json'


def load_remote(api, rid, head, main):
    bundle = validate_bundle(content_at(api, review_path(rid, 'bundle'), head))
    ledger = content_at(api, review_path(rid, 'ledger'), head, optional=True)
    if ledger is None:
        ledger = empty_ledger(bundle)
    baseline = content_at(api, review_path(rid, 'ledger'), main, optional=True)
    validate_ledger(ledger, bundle, baseline)
    return bundle, ledger


def verify_history(api, number, bundle, ledger, trusted, active=True):
    replay = empty_ledger(bundle)
    for entry in ledger['entries']:
        require(entry['pr_number'] == number, 'Cross-PR ledger reuse is forbidden.')
        event = api(f'{PREFIX}/pulls/{number}/reviews/{entry["event_id"]}')
        require(fingerprint(event_snapshot(event)) == entry['event_sha256'],
                'Historical human Review was edited or dismissed; approval is blocked.')
        form = parse_form(event.get('body', ''))
        if active:
            authenticate(api, number, event, entry['actor'], trusted)
        snapshot = validate_bundle(content_at(api, review_path(bundle['review_id'], 'bundle'), event['commit_id']))
        require(fingerprint(snapshot) == fingerprint(bundle), 'Historical approval binds a different bundle.')
        old_policy = policy_at(api, entry['policy_main_sha'])
        require(fingerprint(old_policy) == entry['policy_sha256'], 'Historical accepted policy changed.')
        ancestry = api(f'{PREFIX}/compare/{entry["policy_main_sha"]}...main')
        require(ancestry.get('status') in ('ahead', 'identical'), 'Historical signing policy is not in accepted main.')
        authenticate(api, number, event, entry['actor'], old_policy, current_permissions=active)
        signed_prior = content_at(api, review_path(bundle['review_id'], 'ledger'), event['commit_id'], optional=True)
        if signed_prior is None:
            signed_prior = empty_ledger(bundle)
        require(fingerprint(signed_prior) == fingerprint(replay), 'Signature does not bind its actual prior ledger.')
        verify_anchors(api, bundle, event['commit_id'], entry['policy_main_sha'])
        ensure_gates(api, bundle, form, replay, event['commit_id'], old_policy,
                     today=date.fromisoformat(event['submitted_at'][:10]))
        replay = append_event(bundle, replay, event, form, entry['actor'], number, entry['policy_main_sha'], old_policy)
        require(replay['entries'][-1] == entry, 'Historical entry differs from authenticated state-machine replay.')
    if active and ledger['entries']:
        for axis in ROLES:
            latest = [e for e in ledger['entries'] if e['form']['axis'] == axis]
            if latest and latest[-1]['form']['decision'] in ('approved-scope', 'admitted'):
                validate_form(latest[-1]['form'], bundle, max_age=trusted['policy']['max_regulatory_age_days'])
                require(date.fromisoformat(bundle['validity']['next_review_date']) > datetime.now(timezone.utc).date(),
                        'Signed legal review is overdue.')


def paginate(api, path):
    items = []
    for page in range(1, 101):
        batch = api(path + ('&' if '?' in path else '?') + f'per_page=100&page={page}')
        require(isinstance(batch, list), 'Invalid paginated GitHub response.')
        items.extend(batch)
        if len(batch) < 100:
            return items
    raise ReviewError('GitHub evidence pagination limit exceeded.')


def immutable_history(api, number, bundle, ledger):
    # Existing imported ledgers in any reachable PR commit are immutable even
    # before merge. Force-pushed PRs need a new review PR rather than guessing
    # which disappeared history might still have been effective.
    timeline = paginate(api, f'{PREFIX}/issues/{number}/timeline')
    require(not any(e.get('event') == 'head_ref_force_pushed' for e in timeline),
            'Force-pushed review history cannot be authenticated; use a new review PR.')
    commits = paginate(api, f'{PREFIX}/pulls/{number}/commits')
    count = api(f'{PREFIX}/pulls/{number}').get('commits')
    require(type(count) is int and count <= 250 and len(commits) == count,
            'Complete PR commit history is unavailable or exceeds the 250-commit API limit.')
    for commit in commits:
        prior = content_at(api, review_path(bundle['review_id'], 'ledger'), commit['sha'], optional=True)
        if prior is not None and prior.get('entries'):
            validate_ledger(ledger, bundle, prior)


def verify_anchors(api, bundle, head, main):
    subject_ref = safe_path(bundle['subject_ref'])
    require(subject_ref.startswith('data/reviews/subjects/'), 'Subject must use the accepted subject registry.')
    subject = content_at(api, subject_ref, main)
    require(subject.get('subject_id') == bundle['subject_id'] and subject.get('track') == bundle['track']
            and subject.get('source_revision') == bundle['source_revision']
            and subject.get('source_url', '').startswith('https://github.com/' + bundle['source_repository'] + '/')
            and set(subject.get('review_scope', [])) == set(bundle['review_scope'])
            and set(subject.get('templates', [])) == {v['template_ref'] for v in bundle['template_versions']},
            'Bundle scope, source and full template selection must match the accepted subject.')
    check_ids = set()
    for version in bundle['template_versions']:
        path = safe_path(version['template_ref'])
        require(path.startswith('data/reviews/templates/'), 'Templates must use the accepted template registry.')
        template = content_at(api, path, main)
        require(template.get('template_id') == version['template_id'] and template.get('version') == version['version']
                and fingerprint(template) == version['sha256'], 'Template does not match accepted main version.')
        check_ids.update(c['check_id'] for c in template['checks'])
    require(check_ids == {r['check_id'] for r in bundle['matrix']},
            'Full accepted common and specialized template checks must remain in the matrix.')
    source = api(f'repos/{bundle["source_repository"]}/git/trees/{bundle["source_revision"]}?recursive=1')
    require(source.get('truncated') is False, 'Source tree is incomplete.')
    inventory = {r['path'] for r in source['tree'] if r.get('type') != 'tree'}
    require(set(bundle['review_scope']) | set(bundle['excluded_scope']) == inventory,
            'Selected and excluded files must account for the complete fixed source inventory.')
    files = {r['path']: r['sha'] for r in source['tree'] if r.get('type') == 'blob' and r.get('mode') in ('100644', '100755')}
    require(all(files.get(r['path']) == r['blob_sha'] for r in bundle['source_manifest']),
            'Selected source files do not match the pinned source tree.')
    trees = [api(f'{PREFIX}/git/trees/{ref}?recursive=1') for ref in (main, head)]
    require(all(tree.get('truncated') is False for tree in trees), 'CI trust tree is incomplete.')
    def protected(tree):
        # Only regular v2 JSON records and Markdown review notes may change in a
        # signing PR. This closes Python import/config/action path loopholes that
        # a directory allowlist of validators alone would miss.
        def material(row):
            path = row['path']
            return row.get('type') == 'blob' and row.get('mode') == '100644' and (
                re.fullmatch(r'data/reviews/v2/RV-[A-Za-z0-9-]+/(?:bundle|ledger)\.json', path)
                or re.fullmatch(r'data/reviews/cases/RV-[A-Za-z0-9-]+/(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.(?:json|md)', path)
                or (path.startswith('docs/review-workbench/v2/') and path.endswith('.md')))
        return {r['path']: (r['sha'], r.get('mode'), r.get('type')) for r in tree['tree']
                if r.get('type') != 'tree' and not material(r)}
    require(protected(trees[0]) == protected(trees[1]),
            'Signing PR may change only review data and Markdown review notes; executable inputs must match main.')


def verify_saved_history(bundle, ledger, api=github_api, active=False):
    """Audit local/main history against original PR events, including merged PRs.

    Archived evidence records historical decisions, never a current approval.
    Historical templates/CI and dates use each signature's accepted main commit.
    Active records additionally require current role, permission and freshness.
    """
    validate_bundle(bundle)
    validate_ledger(ledger, bundle)
    if not ledger['entries']:
        return ledger
    numbers = {entry['pr_number'] for entry in ledger['entries']}
    require(len(numbers) == 1, 'A Review ID cannot combine events from different PRs.')
    number = next(iter(numbers))
    pr = api(f'{PREFIX}/pulls/{number}')
    require(pr.get('number') == number and pr.get('base', {}).get('ref') == 'main'
            and pr.get('base', {}).get('repo', {}).get('full_name') == REPOSITORY,
            'Historical events must belong to the repository main review PR.')
    main = main_sha(api)
    trusted = policy_at(api, main)
    immutable_history(api, number, bundle, ledger)
    verify_history(api, number, bundle, ledger, trusted, active=active)
    require(main_sha(api) == main, 'Accepted main policy changed during history validation.')
    return ledger


def online_validate(repository, pr_number, rid, api=github_api):
    require(repository == REPOSITORY, 'Repository is not authorized.')
    pr = pull(api, pr_number)
    main = main_sha(api)
    trusted = policy_at(api, main)
    bundle, ledger = load_remote(api, rid, pr['head']['sha'], main)
    immutable_history(api, pr_number, bundle, ledger)
    verify_anchors(api, bundle, pr['head']['sha'], main)
    verify_history(api, pr_number, bundle, ledger, trusted)
    require(pull(api, pr_number)['head']['sha'] == pr['head']['sha'] and main_sha(api) == main,
            'PR head or main policy changed during validation.')
    return ledger


def append_event(bundle, ledger, event, form, actor, number, main, trusted):
    require(not any(e['event_id'] == event['id'] for e in ledger['entries']), 'This event was already imported.')
    previous_axis = [e for e in ledger['entries'] if e['form']['axis'] == form['axis']]
    require(not previous_axis or previous_axis[-1]['form']['decision'] == 'needs-changes',
            'Terminal human decisions require a new Review ID.')
    entry = {'sequence': len(ledger['entries']) + 1,
             'previous_sha256': ledger['entries'][-1]['entry_sha256'] if ledger['entries'] else None,
             'event_id': event['id'], 'pr_number': number, 'actor': actor, 'event_url': event['html_url'],
             'event_sha256': fingerprint(event_snapshot(event)), 'reviewed_commit_sha': event['commit_id'],
             'policy_main_sha': main, 'policy_sha256': fingerprint(trusted), 'bundle_sha256': fingerprint(bundle),
             'prior_ledger_sha256': fingerprint(ledger), 'submitted_at': event['submitted_at'], 'form': form}
    entry['entry_sha256'] = fingerprint(entry)
    result = deepcopy(ledger)
    result['entries'].append(entry)
    validate_ledger(result, bundle, ledger)
    return result


def cas_write(api, pr, rid, ledger, recheck):
    """Create exactly one ledger update and fast-forward only from the checked head."""
    head = pr['head']['sha']
    commit = api(f'{PREFIX}/git/commits/{head}')
    tree = api(f'{PREFIX}/git/trees', method='POST', payload={
        'base_tree': commit['tree']['sha'], 'tree': [{'path': review_path(rid, 'ledger'),
        'mode': '100644', 'type': 'blob', 'content': json.dumps(ledger, ensure_ascii=False, indent=2) + '\n'}]})
    new_commit = api(f'{PREFIX}/git/commits', method='POST', payload={
        'message': 'chore(review): append authenticated v2 human event', 'tree': tree['sha'], 'parents': [head]})
    recheck()
    # With parent=head and force=false, a concurrent branch advance is not an
    # ancestor of this new commit and GitHub rejects the ref update atomically.
    api(f'{PREFIX}/git/refs/heads/{quote(pr["head"]["ref"], safe="/")}', method='PATCH',
        payload={'sha': new_commit['sha'], 'force': False})


def sync_review(repository, pr_number, review_number, actor, expected_head,
                event_action='submitted', write=False, api=github_api):
    require(repository == REPOSITORY and type(pr_number) is int and pr_number > 0
            and type(review_number) is int and review_number > 0, 'Invalid repository or event identifiers.')
    require(event_action == 'submitted', 'Edited or dismissed Reviews cannot import approval; existing history is blocked.')
    pr = pull(api, pr_number)
    require(pr['head']['sha'] == expected_head, 'PR head changed before synchronization.')
    main = main_sha(api)
    trusted = policy_at(api, main)
    event_path = f'{PREFIX}/pulls/{pr_number}/reviews/{review_number}'
    event = api(event_path)
    require(event.get('id') == review_number, 'Review event ID mismatch.')
    form = authenticate(api, pr_number, event, actor, trusted, expected_head)
    bundle, ledger = load_remote(api, form['review_id'], event['commit_id'], main)
    immutable_history(api, pr_number, bundle, ledger)
    verify_anchors(api, bundle, pr['head']['sha'], main)
    verify_history(api, pr_number, bundle, ledger, trusted)
    existing = [e for e in ledger['entries'] if e['event_id'] == review_number]
    if existing:
        require(existing[0]['event_sha256'] == fingerprint(event_snapshot(event)), 'Replayed event differs from signed history.')
        return ledger
    ensure_gates(api, bundle, form, ledger, expected_head, trusted)
    result = append_event(bundle, ledger, event, form, actor, pr_number, main, trusted)

    def recheck():
        require(pull(api, pr_number)['head']['sha'] == expected_head and main_sha(api) == main,
                'Concurrent head or policy update; retry against the new state.')
        require(fingerprint(event_snapshot(api(event_path))) == fingerprint(event_snapshot(event)),
                'Review changed during synchronization.')
        authenticate(api, pr_number, api(event_path), actor, trusted, expected_head)
        verify_history(api, pr_number, bundle, ledger, trusted)
        ensure_gates(api, bundle, form, ledger, expected_head, trusted)
    recheck()
    if write:
        cas_write(api, pr, form['review_id'], result, recheck)
    return result


def git_output(root, args):
    try:
        result = subprocess.run(['git', '-C', str(root), *args], capture_output=True,
                                text=True, timeout=30, check=True)
        return result.stdout
    except (OSError, subprocess.SubprocessError):
        raise ReviewError('Trusted Git baseline could not be read.') from None


def validate_local(root, base_ref=None, online=False, api=github_api):
    root = Path(root).resolve()
    records = root / V2_DIRECTORY
    require(not records.is_symlink() and not (root / 'data').is_symlink()
            and not (root / 'data/reviews').is_symlink(), 'Symlink review directories are forbidden.')
    if records.exists():
        require(all(p.is_dir() and not p.is_symlink() and RID.fullmatch(p.name) for p in records.iterdir()),
                'Unexpected v2 review directory entry.')
    bundles = {}
    ledgers = {}
    for path in sorted(records.glob('RV-*/*')):
        require(path.name in ('bundle.json', 'ledger.json') and not path.is_symlink()
                and not path.parent.is_symlink() and path.is_file(), 'Unexpected v2 review material or symlink.')
        rid = path.parent.name
        require(RID.fullmatch(rid), 'Invalid review directory ID.')
        value = loads(path.read_text())
        require(value.get('review_id') == rid, 'Review directory and ID differ.')
        (bundles if path.name == 'bundle.json' else ledgers)[rid] = value
    require(set(ledgers) <= set(bundles), 'Orphan ledger without a review bundle.')
    for rid, bundle in bundles.items():
        validate_bundle(bundle)
        if rid in ledgers:
            validate_ledger(ledgers[rid], bundle)
    if base_ref:
        require(not base_ref.startswith('-'), 'Invalid Git baseline reference.')
        base = git_output(root, ['rev-parse', '--verify', base_ref + '^{commit}']).strip()
        require(SHA.fullmatch(base), 'Invalid Git baseline commit.')
        paths = git_output(root, ['ls-tree', '-r', '--name-only', base, '--', V2_DIRECTORY]).splitlines()
        for path in paths:
            if not path.endswith('/ledger.json'):
                continue
            prior = loads(git_output(root, ['show', base + ':' + path]))
            if not prior.get('entries'):
                continue
            rid = prior['review_id']
            require(rid in bundles and rid in ledgers, 'Signed history cannot be deleted.')
            old_bundle = loads(git_output(root, ['show', base + ':' + review_path(rid, 'bundle')]))
            require(old_bundle == bundles[rid], 'Signed bundle cannot be changed; use a new Review ID.')
            validate_ledger(ledgers[rid], bundles[rid], prior)
    if online:
        signed = {rid: ledger for rid, ledger in ledgers.items() if ledger['entries']}
        if signed:
            main = main_sha(api)
            for rid, ledger in signed.items():
                accepted = content_at(api, review_path(rid, 'ledger'), main, optional=True)
                verify_saved_history(bundles[rid], ledger, api, active=(accepted != ledger))
    return len(bundles)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    validate = sub.add_parser('validate')
    validate.add_argument('--root', type=Path, default=ROOT)
    validate.add_argument('--base-ref', default=None)
    validate.add_argument('--online', action='store_true')
    form = sub.add_parser('form')
    form.add_argument('--bundle', type=Path, required=True)
    form.add_argument('--axis', choices=ROLES, default='professional_review')
    sync = sub.add_parser('sync-review')
    sync.add_argument('--repository', default=REPOSITORY)
    sync.add_argument('--pr', type=int, required=True)
    sync.add_argument('--review', type=int, required=True)
    sync.add_argument('--actor', required=True)
    sync.add_argument('--expected-head', required=True)
    sync.add_argument('--event-action', choices=('submitted', 'edited', 'dismissed'), default='submitted')
    sync.add_argument('--write', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'validate':
            count = validate_local(args.root, args.base_ref, args.online)
            print(f'V2 validation passed: {count} bundles; structural checks alone never authenticate a human.')
        elif args.command == 'form':
            print(render_form(loads(args.bundle.read_text()), args.axis), end='')
        else:
            result = sync_review(args.repository, args.pr, args.review, args.actor, args.expected_head,
                                 args.event_action, args.write)
            print('V2 authenticated ledger ' + ('written' if args.write else 'validated (dry run)') +
                  f': {len(result["entries"])} events.')
    except (ReviewError, KeyError, TypeError, OSError) as exc:
        print('V2 review blocked: ' + (str(exc) if isinstance(exc, ReviewError) else 'Malformed or unavailable input.'), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
