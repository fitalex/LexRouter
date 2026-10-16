"""Synthetic positive/negative handoffs; never execute or import upstream code."""

import copy
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_p1_handoff import (handoff_schema, manifest_schema, inventory_tree_sha,
                                 validate)  # noqa: E402
from validate_p1_readiness import fingerprint  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402


class HandoffTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.cp, self.rp, self.ip, self.hp = [self.root / (x + '.json') for x in ('c', 'r', 'i', 'h')]
        self.c = json.loads((ROOT / 'tests/fixtures/p1-readiness/candidates.json').read_text())
        self.a = json.loads((ROOT / 'tests/fixtures/p1-readiness/valid.json').read_text())
        self.i = json.loads((ROOT / 'tests/fixtures/intake/valid.json').read_text())
        a, p = self.a['records'][0], self.i['records'][0]
        cid = a['candidate_id']
        self.m = dict(format_version=1, candidate_id=cid, revision=a['revision'], tree_sha='a'*40,
                      files=[dict(path=name, blob_sha='b'*40, mode='100644', file_type='md',
                                  role='synthetic', purpose='Synthetic fixture.', content_review='read',
                                  decision='eligible-for-scope-review', basis='synthetic-only')
                             for name in ('SKILL.md', 'README.md', 'LICENSE')])
        self.m['tree_sha'] = inventory_tree_sha(self.m['files'])
        self.h = dict(format_version=1, task='LR-P0-05', records=[dict(
            candidate_id=cid, readiness_snapshot_sha256=fingerprint(a),
            intake_snapshot_sha256=fingerprint(p), revision=a['revision'],
            manifest=f'data/reviews/manifests/{cid}.json', manifest_sha256=fingerprint(self.m),
            tree_file_count=3, tree_sha=self.m['tree_sha'], hosting_status='not-approved',
            professional_status='not-performed', catalog_status='not-admitted',
            regulatory_currency={k:a['regulatory_currency'][k] for k in ('status','as_of')},
            unresolved_issues=[dict(kind=k, owner=o, action='Synthetic pending action.')
                               for k,o in [('rights','Human Maintainer'),('dependency','engineering-maintainer')]],
            professional_todos=[dict(owner='legal-professional', action=t)
                                for t in a['professional_review']['required_checks']], handoff_section=cid)])
        self.mp = self.root / self.r['manifest']
        self.mp.parent.mkdir(parents=True)

    @property
    def r(self):
        return self.h['records'][0]

    def save(self):
        for path, data in [(self.cp,self.c),(self.rp,self.a),(self.ip,self.i),(self.hp,self.h),(self.mp,self.m)]:
            path.write_text(json.dumps(data), encoding='utf-8')

    def result(self):
        self.save()
        return validate(self.hp, self.cp, self.rp, self.ip, self.root)

    def rejected(self, text):
        errors = self.result()[1]
        self.assertTrue(errors)
        self.assertIn(text, '\n'.join(errors))

    def test_synthetic_positive_and_schema(self):
        for schema in (handoff_schema(), manifest_schema()):
            Draft202012Validator.check_schema(schema)
        self.assertEqual(self.result(), (1, []))

    def test_production_and_synthetic_cli(self):
        self.save()
        for args in ([], [str(self.hp), '--candidates', str(self.cp), '--readiness', str(self.rp),
                          '--intake', str(self.ip), '--root', str(self.root)]):
            p = subprocess.run([sys.executable,str(ROOT/'scripts/validate_p1_handoff.py'),*args],
                               cwd=ROOT, capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertIn('No hosting approval or professional review',p.stdout)
        self.r['hosting_status']='hosted'; self.save()
        p=subprocess.run([sys.executable,str(ROOT/'scripts/validate_p1_handoff.py'),str(self.hp)],
                         cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(p.returncode,1)
        self.assertIn('/records/0/hosting_status',p.stderr)

    def test_all_approval_states_and_currency_fail_closed(self):
        original=copy.deepcopy(self.h)
        for field in ('hosting_status','professional_status','catalog_status'):
            for value in ('approved','hosted','completed',True,None):
                self.h=copy.deepcopy(original);self.r[field]=value
                self.rejected(field)
        for field,value in [('status','verified'),('as_of','2026-10-16')]:
            self.h=copy.deepcopy(original);self.r['regulatory_currency'][field]=value
            self.rejected(field)
        self.h=copy.deepcopy(original);self.r['reviewer']='invented'
        self.rejected('Additional properties')

    def test_required_fields_and_invalid_shapes(self):
        original=copy.deepcopy(self.h)
        for field in original['records'][0]:
            self.h=copy.deepcopy(original);del self.r[field];self.rejected(field)
        for value in (None,[],{**original,'records':[]},{**original,'format_version':True}):
            self.h=value;self.rejected('/')
        self.h=copy.deepcopy(original);self.r['unresolved_issues'][0]['action']=' '
        self.rejected('action')

    def test_unknown_duplicate_missing_or_external_candidate(self):
        original=copy.deepcopy(self.h)
        self.r['candidate_id']='unknown';self.rejected('curated-hosting')
        self.h=copy.deepcopy(original);self.h['records'].append(copy.deepcopy(self.r));self.rejected('duplicate candidate')
        self.h=copy.deepcopy(original);self.i['records'][0]['proposed_track']='external-reference'
        self.r['intake_snapshot_sha256']=fingerprint(self.i['records'][0]);self.rejected('curated-hosting')

    def test_prior_audit_proposal_and_revision_drift(self):
        original=copy.deepcopy(self.h)
        for field in ('readiness_snapshot_sha256','intake_snapshot_sha256','revision'):
            self.h=copy.deepcopy(original);self.r[field]='c'*len(self.r[field]);self.rejected(field)
        self.h=copy.deepcopy(original);self.c['candidates'][0]['description']+=' changed'
        self.rejected('re-audit')

    def test_original_blockers_cannot_be_upgraded(self):
        self.i['records'][0]['approvals']['authorization']='approved'
        self.rejected('authorization')

    def test_scope_decisions_and_unread_eligibility(self):
        original=copy.deepcopy(self.m)
        for value in ('approved','hosted','',None):
            self.m=copy.deepcopy(original);self.m['files'][0]['decision']=value;self.rejected('decision')
        self.m=copy.deepcopy(original);self.m['files'][0]['content_review']='not-read'
        self.r['manifest_sha256']=fingerprint(self.m);self.rejected('unread')
        for decision in ('requires-authorization','exclude-from-hosting','unverified'):
            self.m=copy.deepcopy(original);self.m['files'][0]['decision']=decision
            self.r['manifest_sha256']=fingerprint(self.m);self.assertEqual(self.result(),(1,[]))

    def test_inventory_digest_count_identity_and_core_files(self):
        original=copy.deepcopy(self.m)
        self.m['files'][0]['basis']='changed';self.rejected('inventory changed')
        self.m=copy.deepcopy(original);self.r['tree_file_count']=4;self.rejected('count')
        self.r['tree_file_count']=3;self.m['candidate_id']='other';self.rejected('original revision')
        self.m=copy.deepcopy(original);self.m['files'].pop();self.rejected('entry, license and README')
        self.m=copy.deepcopy(original);self.m['files'].append(copy.deepcopy(self.m['files'][0]));self.rejected('duplicate source path')

    def test_path_blob_mode_changes_cannot_hide_behind_new_digest(self):
        original=copy.deepcopy(self.m)
        for field,value in [('path','replaced.md'),('blob_sha','d'*40),('mode','100755')]:
            self.m=copy.deepcopy(original);self.m['files'][0][field]=value
            self.r['manifest_sha256']=fingerprint(self.m);self.rejected('fixed Git tree')
        self.m=copy.deepcopy(original);self.m['files'][0]['blob_sha']='d'*40
        self.m['tree_sha']=inventory_tree_sha(self.m['files']);self.r['tree_sha']=self.m['tree_sha']
        self.r['manifest_sha256']=fingerprint(self.m);self.rejected('existing fixed audit')

    def test_unsafe_paths_wildcards_and_symlinks(self):
        original=copy.deepcopy(self.m)
        for value in ('/tmp/file','../file','a/../b','a\\b','refs/*','refs/[a]','a//b'):
            self.m=copy.deepcopy(original);self.m['files'][0]['path']=value;self.rejected('/')
        self.m=copy.deepcopy(original);self.r['manifest']='../../outside.json';self.rejected('manifest')
        self.r['manifest']='data/reviews/manifests/synthetic-p1-review.json'
        self.save();self.mp.unlink();self.mp.symlink_to('/tmp/outside-handoff.json')
        self.assertIn('within the repository','\n'.join(validate(self.hp,self.cp,self.rp,self.ip,self.root)[1]))

    def test_missing_professional_checks_and_responsibilities(self):
        original=copy.deepcopy(self.h)
        self.r['professional_todos'][0]['action']='replacement';self.rejected('original professional checks')
        self.h=copy.deepcopy(original);self.r['unresolved_issues'].pop();self.rejected('rights and dependency')
        self.h=copy.deepcopy(original);self.r['unresolved_issues'][0]['owner']='legal-professional';self.rejected('engineering roles')

    def test_bad_json_encoding_missing_files_and_duplicate_keys(self):
        for path in (self.hp,self.cp,self.rp,self.ip,self.mp):
            for raw in (b'{',b'{"x":1,"x":2}',b'{"x":NaN}',b'\xff'):
                self.save();path.write_bytes(raw)
                self.assertTrue(validate(self.hp,self.cp,self.rp,self.ip,self.root)[1])
            self.save();path.unlink()
            self.assertTrue(validate(self.hp,self.cp,self.rp,self.ip,self.root)[1])

    def test_no_network(self):
        self.save()
        with patch.object(socket,'socket',side_effect=AssertionError('network forbidden')):
            self.assertEqual(validate(self.hp,self.cp,self.rp,self.ip,self.root),(1,[]))


if __name__=='__main__':
    unittest.main()
