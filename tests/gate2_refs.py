"""Read-only CI reference selection; never use mutable branch names as fixtures."""
import re


def resolve(pr, main, event_pr='', event_head=''):
    if pr['base']['repo']['full_name'] != 'fitalex/LexRouter' or pr['base']['ref'] != 'main':
        raise ValueError('Unexpected review repository or base')
    state = 'merged' if pr.get('merged') else pr['state']
    if state not in ('open', 'closed', 'merged'):
        raise ValueError('Unknown PR lifecycle state')
    # Closed/merged PR objects retain immutable commit IDs even after branch deletion.
    head = pr.get('merge_commit_sha') if state == 'merged' else pr['head']['sha']
    if str(pr['number']) == str(event_pr):
        head = event_head
        state = 'event-head'
    if not all(isinstance(ref, str) and re.fullmatch(r'[0-9a-f]{40}', ref) for ref in (head, main)):
        raise ValueError('Missing immutable commit; restore snapshot explicitly, never skip')
    return {'head': head, 'main': main, 'state': state,
            'active': 'true' if pr['state'] == 'open' and not pr.get('merged') else 'false'}
