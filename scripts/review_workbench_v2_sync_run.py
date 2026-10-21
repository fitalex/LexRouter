#!/usr/bin/env python3
"""Trusted workflow_run bridge. Signal artifacts and PR code are never consumed."""

import argparse
import re
import sys

import review_workbench_v2 as v2

REPOSITORY = 'fitalex/LexRouter'
SIGNAL_PATH = '.github/workflows/review-v2-signal.yml'
LEDGER_PATH = re.compile(r'^data/reviews/v2/(RV-[A-Za-z0-9-]+)/ledger\.json$')


def sync_run(run_id, *, write=False, api=None):
    api = api or v2.github_api
    prefix = f'repos/{REPOSITORY}'
    run = api(f'{prefix}/actions/runs/{run_id}')
    if (run.get('id') != run_id or run.get('event') != 'pull_request_review'
            or run.get('path') != SIGNAL_PATH or run.get('status') != 'completed'
            or run.get('conclusion') != 'success'
            or run.get('head_repository', {}).get('full_name') != REPOSITORY):
        raise v2.ReviewError('Untrusted review signal.')
    associations = run.get('pull_requests', [])
    if len(associations) != 1:
        raise v2.ReviewError('Review signal must identify exactly one pull request.')
    number = associations[0].get('number')
    if type(number) is not int or number < 1:
        raise v2.ReviewError('Invalid signal pull request.')
    pr = api(f'{prefix}/pulls/{number}')
    if (pr.get('state') != 'open' or pr.get('base', {}).get('ref') != 'main'
            or pr.get('head', {}).get('repo', {}).get('full_name') != REPOSITORY
            or pr.get('base', {}).get('repo', {}).get('full_name') != REPOSITORY):
        raise v2.ReviewError('Review sync requires an open same-repository main PR.')
    head = pr['head']['sha']
    accepted_main = v2.main_sha(api)
    tree = api(f'{prefix}/git/trees/{head}?recursive=1')
    base_tree = api(f'{prefix}/git/trees/{accepted_main}?recursive=1')
    if tree.get('truncated') or not isinstance(tree.get('tree'), list):
        raise v2.ReviewError('Incomplete review tree.')
    if base_tree.get('truncated') or not isinstance(base_tree.get('tree'), list):
        raise v2.ReviewError('Incomplete accepted review tree.')
    review_ids = []
    for item in tree['tree']:
        match = LEDGER_PATH.fullmatch(item.get('path', ''))
        if match:
            if item.get('type') != 'blob' or item.get('mode') != '100644':
                raise v2.ReviewError('Ledger must be a regular JSON file.')
            review_ids.append(match[1])
    accepted_ids = {m[1] for item in base_tree['tree']
                    if (m := LEDGER_PATH.fullmatch(item.get('path', '')))}
    if accepted_ids - set(review_ids):
        raise v2.ReviewError('Accepted ledger was deleted.')
    # A normal commit may delete an entire unmerged review directory. Enumerate
    # the PR's preceding trees too: current-tree-only scanning loses that ID.
    commits = v2.paginate(api, f'{prefix}/pulls/{number}/commits')
    if (type(pr.get('commits')) is not int or pr['commits'] >= 250
            or len(commits) != pr['commits']):
        raise v2.ReviewError('PR commit history exceeds GitHub complete-list limit.')
    known_ids = set(review_ids)
    tree_cache = {head: tree, accepted_main: base_tree}
    for commit in commits:
        sha = commit.get('sha', '')
        if not v2.SHA.fullmatch(sha):
            raise v2.ReviewError('Invalid PR history commit.')
        prior_tree = tree_cache.get(sha)
        if prior_tree is None:
            prior_tree = api(f'{prefix}/git/trees/{sha}?recursive=1')
            tree_cache[sha] = prior_tree
        if prior_tree.get('truncated') or not isinstance(prior_tree.get('tree'), list):
            raise v2.ReviewError('Incomplete PR history tree.')
        known_ids.update(m[1] for item in prior_tree['tree']
                         if (m := LEDGER_PATH.fullmatch(item.get('path', ''))))
    if known_ids - set(review_ids):
        raise v2.ReviewError('Unmerged review history was deleted; preserve the original record.')
    # Always recheck old events, including on edited/dismissed signals, before
    # looking for new decisions. A failure preserves the old ledger and blocks.
    for rid in sorted(review_ids):
        path = f'data/reviews/v2/{rid}/ledger.json'
        accepted = v2.content_at(api, path, accepted_main, optional=True)
        if accepted and accepted.get('entries'):
            current = v2.content_at(api, path, head)
            bundle_path = f'data/reviews/v2/{rid}/bundle.json'
            if (current != accepted or v2.content_at(api, bundle_path, head)
                    != v2.content_at(api, bundle_path, accepted_main)):
                raise v2.ReviewError('Accepted signed reviews are immutable; create a new Review ID.')
            continue  # Other PRs' accepted records retain their original event identity.
        v2.online_validate(REPOSITORY, number, rid, api=api)
    if run.get('head_sha') not in (head, pr.get('merge_commit_sha')):
        if write and review_ids:
            # Retry can repair a dispatch outage after a successful ledger CAS.
            # Every surviving ledger was authenticated above; no new event is imported.
            api(f'{prefix}/actions/workflows/validate-skills.yml/dispatches', method='POST',
                payload={'ref': pr['head']['ref']})
        return 0  # stale wake-up: old events were still audited above
    reviews = []
    for page in range(1, 101):
        batch = api(f'{prefix}/pulls/{number}/reviews?per_page=100&page={page}')
        if not isinstance(batch, list):
            raise v2.ReviewError('Invalid review list.')
        reviews.extend(batch)
        if len(batch) < 100:
            break
    else:
        raise v2.ReviewError('Review pagination exceeded bounded limit.')
    if v2.main_sha(api) != accepted_main:
        raise v2.ReviewError('Accepted main changed during synchronization.')
    trusted = v2.policy_at(api, accepted_main)
    pending = []
    for review in reviews:
        if review.get('commit_id') != head or 'lexrouter-review-v2' not in (review.get('body') or ''):
            continue
        user = review.get('user', {})
        roles = trusted['roles'].get('reviewers', {}).get(user.get('login'), [])
        if user.get('type') != 'User' or not set(v2.ROLES.values()).intersection(roles):
            continue  # Public, unassigned comments cannot suppress a real signature.
        v2.authenticate(api, number, review, user.get('login'), trusted, head)
        pending.append(review)
    # Multiple decisions at the same head are not silently reordered. After a
    # single append, another independent decision must review the new ledger.
    if len(pending) > 1:
        raise v2.ReviewError('Concurrent decisions require a fresh reviewed head.')
    for review in pending:
        if review.get('state') != 'COMMENTED':
            raise v2.ReviewError('Decision must be an active Comment Review.')
        v2.sync_review(REPOSITORY, number, review['id'],
                       review.get('user', {}).get('login'), head,
                       event_action='submitted', write=write, api=api)
    if pending and write:
        # GITHUB_TOKEN commits do not start push/PR workflows. Explicit dispatch
        # supplies CI for the new ledger commit before the independent decision.
        api(f'{prefix}/actions/workflows/validate-skills.yml/dispatches', method='POST',
            payload={'ref': pr['head']['ref']})
    return len(pending)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', type=int, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.run_id < 1:
            raise v2.ReviewError('Invalid workflow run ID.')
        count = sync_run(args.run_id, write=args.write)
        print(f'Validated review signal; {count} current decision(s) processed.')
        return 0
    except (v2.ReviewError, KeyError, TypeError, ValueError):
        print('Review synchronization refused; no unverified decision accepted.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
