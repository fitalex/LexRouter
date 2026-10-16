"""Adversarial proposal checks with synthetic audit inputs; no upstream execution."""

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
from validate_intake_plan import intake_schema, validate  # noqa: E402
from validate_p1_readiness import fingerprint  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402

CLI = ROOT / "scripts/validate_intake_plan.py"


class IntakeTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "intake.json"
        self.cp = Path(folder.name) / "candidates.json"
        self.rp = Path(folder.name) / "readiness.json"
        self.data = json.loads((ROOT / "tests/fixtures/intake/valid.json").read_text())
        self.candidates = json.loads((ROOT / "tests/fixtures/p1-readiness/candidates.json").read_text())
        self.audit = json.loads((ROOT / "tests/fixtures/p1-readiness/valid.json").read_text())

    @property
    def record(self):
        return self.data["records"][0]

    @property
    def opportunity(self):
        return self.data["original_opportunities"][0]

    def save(self):
        for path, data in ((self.path, self.data), (self.cp, self.candidates), (self.rp, self.audit)):
            path.write_text(json.dumps(data), encoding="utf-8")

    def result(self):
        self.save()
        return validate(self.path, self.cp, self.rp)

    def rejected(self, field):
        _, errors = self.result()
        self.assertTrue(errors, "invalid proposal unexpectedly passed")
        self.assertIn(field, "\n".join(errors))

    def blocked(self):
        audit = self.audit["records"][0]
        audit.update(p1_status="blocked", blockers=[dict(
            code="synthetic-rights-gap", evidence="Synthetic scope gap.",
            evidence_urls=[audit["source_url"]], impact="Cannot establish permission.",
            next_action="Maintainer decides clarification path.", owner="Human Maintainer")])
        audit["authorization_review"]["status"] = "scope-unclear"
        self.record.update(proposed_track="external-reference", readiness_snapshot_sha256=fingerprint(audit))
        self.record["approvals"]["authorization"] = "blocked"

    def test_synthetic_positive_tracks_and_no_inheritance(self):
        Draft202012Validator.check_schema(intake_schema())
        self.assertEqual(self.result(), (1, []))
        self.blocked()
        # B remains pending, even though its background third-party ID is blocked.
        self.assertEqual(self.opportunity["approvals"]["authorization"], "pending")
        self.assertEqual(self.result(), (1, []))
        self.data["original_opportunities"] = []
        self.assertEqual(self.result(), (1, []))

    def test_actual_and_synthetic_cli(self):
        self.save()
        for args in ([], [str(self.path), "--candidates", str(self.cp), "--readiness", str(self.rp)]):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(CLI), *args], cwd=ROOT,
                                        capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("No hosting, legal, catalog", result.stdout)

    def test_unknown_duplicate_and_missing_candidate_links(self):
        original = copy.deepcopy(self.data)
        self.record["candidate_id"] = "unknown-candidate"
        self.rejected("unknown candidate ID")
        self.data = copy.deepcopy(original)
        self.data["records"].append(copy.deepcopy(self.record))
        self.rejected("duplicate candidate ID")
        self.data = copy.deepcopy(original)
        self.opportunity["related_candidate_ids"] = ["unknown-candidate"]
        self.rejected("related_candidate_ids")
        self.data = copy.deepcopy(original)
        self.record["candidate_id"] = "replacement-candidate"
        self.rejected("missing candidate IDs")

    def test_proposal_modes_and_required_gates(self):
        original = copy.deepcopy(self.data)
        for value in ("A", "hosted", "original-development", None):
            self.data = copy.deepcopy(original)
            self.record["proposed_track"] = value
            self.rejected("proposed_track")
        for section in ("records", "original_opportunities"):
            self.data = copy.deepcopy(original)
            record = self.data[section][0]
            for gate in list(record["required_gates"]):
                with self.subTest(section=section, gate=gate):
                    record["required_gates"].remove(gate)
                    self.rejected("required_gates")
                    record["required_gates"].append(gate)

    def test_blocked_candidate_cannot_upgrade_or_receive_hosting_proposal(self):
        self.blocked()
        self.record["approvals"]["authorization"] = "pending"
        self.rejected("must preserve audit blocking status")
        self.record["approvals"]["authorization"] = "blocked"
        self.record["proposed_track"] = "curated-hosting"
        self.rejected("must remain external-reference")

    def test_every_approval_axis_rejects_claimed_completion(self):
        original = copy.deepcopy(self.data)
        for blocked in (False, True):
            for section in ("records", "original_opportunities"):
                for field in original[section][0]["approvals"]:
                    with self.subTest(blocked=blocked, section=section, field=field):
                        self.data = copy.deepcopy(original)
                        if blocked:
                            self.blocked()
                        self.data[section][0]["approvals"][field] = "approved"
                        self.rejected(field)

    def test_copy_and_redistribution_fail_closed_for_all_tracks(self):
        original = copy.deepcopy(self.data)
        for blocked in (False, True):
            for section in ("records", "original_opportunities"):
                for right in ("copy", "redistribute"):
                    for value in (True, "false", 0):
                        with self.subTest(blocked=blocked, section=section, right=right, value=value):
                            self.data = copy.deepcopy(original)
                            if blocked:
                                self.blocked()
                            self.data[section][0]["permissions"][right] = value
                            self.rejected(right)

    def test_original_ids_permissions_and_completion_are_independent(self):
        original = copy.deepcopy(self.data)
        for field, value in (("opportunity_id", self.record["candidate_id"]),
                             ("authorization_basis", "verified"),
                             ("development_status", "completed"),
                             ("proposed_track", "curated-hosting")):
            self.data = copy.deepcopy(original)
            self.opportunity[field] = value
            self.rejected(field)
        self.data = copy.deepcopy(original)
        self.data["original_opportunities"].append(copy.deepcopy(self.opportunity))
        self.rejected("duplicate or third-party ID")
        self.data = copy.deepcopy(original)
        self.blocked()
        self.opportunity["approvals"]["authorization"] = "blocked"
        self.rejected("cannot inherit third-party authorization")

    def test_audit_changes_require_proposal_review_and_reuse_existing_checks(self):
        self.audit["records"][0]["follow_up"][0]["action"] += " New review scope."
        self.rejected("audit changed; re-review proposal")
        self.record["readiness_snapshot_sha256"] = fingerprint(self.audit["records"][0])
        self.assertEqual(self.result(), (1, []))
        self.candidates["candidates"][0]["description"] += " Source changed."
        self.rejected("candidate changed; re-audit")

    def test_required_fields_types_nonblank_and_no_extra_evidence(self):
        original = copy.deepcopy(self.data)
        for section in ("records", "original_opportunities"):
            for field in original[section][0]:
                self.data = copy.deepcopy(original)
                del self.data[section][0][field]
                self.rejected(field)
            for owner in ("Human Maintainer", "legal-professional", "engineering-maintainer"):
                self.data = copy.deepcopy(original)
                item = self.data[section][0]
                item["next_actions"] = [a for a in item["next_actions"] if a["owner"] != owner]
                self.rejected("responsibilities")
        for data in (None, [], {**original, "records": []}, {**original, "format_version": True}):
            self.data = data
            self.rejected("/")
        self.data = copy.deepcopy(original)
        self.record["authorization_basis"]["license"] = "MIT"
        self.rejected("Additional properties")
        self.data = copy.deepcopy(original)
        self.record["business_value_and_rationale"] = "  "
        self.rejected("business_value_and_rationale")

    def test_malformed_json_missing_files_utf8_and_cli_errors(self):
        for path in (self.path, self.cp, self.rp):
            for raw in ('{"records":', '{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
                self.save()
                path.write_text(raw)
                count, errors = validate(self.path, self.cp, self.rp)
                self.assertTrue(errors, (path, raw, count))
                self.assertIn(str(path), "\n".join(errors))
            self.save()
            path.write_bytes(b"\xff")
            self.assertTrue(validate(self.path, self.cp, self.rp)[1])
            path.unlink()
            self.assertTrue(validate(self.path, self.cp, self.rp)[1])
        self.save()
        self.record["permissions"]["copy"] = True
        self.save()
        result = subprocess.run([sys.executable, str(CLI), str(self.path),
                                 "--candidates", str(self.cp), "--readiness", str(self.rp)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("/records/0/permissions/copy", result.stderr)
        self.assertIn("FAIL:", result.stderr)

    def test_validation_needs_no_network(self):
        self.save()
        with patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            self.assertEqual(validate(self.path, self.cp, self.rp), (1, []))


if __name__ == "__main__":
    unittest.main()
