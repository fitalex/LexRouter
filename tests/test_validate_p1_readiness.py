"""Offline adversarial tests using synthetic sources; no third-party execution."""

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
from validate_p1_readiness import fingerprint, validate  # noqa: E402

CLI = ROOT / "scripts/validate_p1_readiness.py"
FIXTURES = ROOT / "tests/fixtures/p1-readiness"


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "readiness.json"
        self.candidates_path = Path(self.folder.name) / "candidates.json"
        self.data = json.loads((FIXTURES / "valid.json").read_text())
        self.candidates = json.loads((FIXTURES / "candidates.json").read_text())

    @property
    def record(self):
        return self.data["records"][0]

    @property
    def candidate(self):
        return self.candidates["candidates"][0]

    def save(self):
        self.path.write_text(json.dumps(self.data), encoding="utf-8")
        self.candidates_path.write_text(json.dumps(self.candidates), encoding="utf-8")

    def result(self):
        self.save()
        return validate(self.path, self.candidates_path)

    def rejected(self, field):
        _, errors = self.result()
        self.assertTrue(errors, "invalid record unexpectedly passed")
        self.assertIn(field, "\n".join(errors))

    def blocker(self):
        return dict(code="synthetic-blocker", evidence="Synthetic conflicting statements.",
                    evidence_urls=[self.record["source_url"]], impact="Cannot establish permission.",
                    next_action="Obtain rightsholder clarification.", owner="upstream-rightsholder")

    def test_positive_ready_blocked_rejected_and_pending_currency(self):
        self.assertEqual(self.result(), (1, []))
        self.record["blockers"] = [self.blocker()]
        for status in ("blocked", "rejected"):
            with self.subTest(status=status):
                self.record["p1_status"] = status
                self.assertEqual(self.result(), (1, []))
        for item in (self.record, self.candidate):
            item["regulatory_currency"]["status"] = "pending-verification"
        self.record["candidate_snapshot_sha256"] = fingerprint(self.candidate)
        self.assertEqual(self.result(), (1, []))

    def test_cli_actual_default_and_explicit_synthetic_pair(self):
        self.save()
        for args in ([], [str(self.path), "--candidates", str(self.candidates_path)]):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(CLI), *args], cwd=ROOT,
                                        capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("PASS:", result.stdout)
                self.assertIn("No legal/license verification or intake approval", result.stdout)

    def test_unknown_duplicate_and_omitted_candidates(self):
        original = copy.deepcopy(self.data)
        self.record["candidate_id"] = "unknown-candidate"
        self.rejected("unknown candidate ID")
        self.data = copy.deepcopy(original)
        self.data["records"].append(copy.deepcopy(self.record))
        self.rejected("duplicate candidate ID")
        self.data = copy.deepcopy(original)
        extra = copy.deepcopy(self.candidate)
        extra["candidate_id"] = "omitted-candidate"
        self.candidates["candidates"].append(extra)
        self.rejected("missing candidate IDs: omitted-candidate")

    def test_empty_or_malformed_manifest_cannot_claim_coverage(self):
        for data in (None, [], {"format_version": 1},
                     {**self.data, "records": []}, {**self.data, "records": [None]},
                     {**self.data, "format_version": True}, {**self.data, "unexpected": True}):
            with self.subTest(data=data):
                self.data = data
                self.rejected("/")

    def test_required_fields_and_nested_fields_are_enforced(self):
        original = copy.deepcopy(self.data)

        def required_paths(obj, path=()):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    yield (*path, key)
                    yield from required_paths(value, (*path, key))
            elif isinstance(obj, list):
                for index, value in enumerate(obj):
                    yield from required_paths(value, (*path, index))

        # Include the issue object, which is absent from the ready fixture.
        original["records"][0].update(p1_status="blocked", blockers=[self.blocker()])
        for parts in required_paths(original):
            with self.subTest(parts=parts):
                self.data = copy.deepcopy(original)
                target = self.data
                for part in parts[:-1]:
                    target = target[part]
                del target[parts[-1]]
                self.rejected(str(parts[-1]))

    def test_bad_status_types_dates_urls_and_owners(self):
        original = copy.deepcopy(self.data)
        for field, value in (("p1_status", "approved"), ("p1_status", None),
                             ("revision", "main"), ("business_categories", []),
                             ("source_url", "http://example.com/unpinned"),
                             ("candidate_snapshot_sha256", "bad")):
            with self.subTest(field=field):
                self.data = copy.deepcopy(original)
                self.record[field] = value
                self.rejected(field)
        self.data = copy.deepcopy(original)
        self.data["audited_at"] = "2026-02-30"
        self.rejected("audited_at")
        self.data = copy.deepcopy(original)
        self.record["follow_up"][0]["owner"] = "someone"
        self.rejected("owner")
        self.data = copy.deepcopy(original)
        self.record["follow_up"] = [self.record["follow_up"][0]]
        self.rejected("must assign maintainer decisions and legal professional review")

    def test_blocked_and_rejected_require_actionable_reason(self):
        for status in ("blocked", "rejected"):
            self.record["p1_status"] = status
            self.rejected("blockers")
        self.record["blockers"] = [self.blocker()]
        for field in ("evidence", "impact", "next_action", "owner"):
            with self.subTest(field=field):
                item = self.blocker()
                item[field] = "  "
                self.record["blockers"] = [item]
                self.rejected(field)

    def test_ready_cannot_hide_unresolved_authorization_or_entry(self):
        original = copy.deepcopy(self.data)
        for status in ("missing-license", "conflicting", "restricted", "scope-unclear"):
            with self.subTest(status=status):
                self.record["authorization_review"]["status"] = status
                self.rejected("ready requires")
        self.data = copy.deepcopy(original)
        self.record["blockers"] = [self.blocker()]
        self.rejected("ready records cannot")
        for workflow in ("orchestration-only", "insufficient-evidence", "out-of-scope"):
            self.data = copy.deepcopy(original)
            self.record["source_review"]["workflow_status"] = workflow
            self.rejected("ready requires")
        self.data = copy.deepcopy(original)
        self.record["source_review"]["entry_exists"] = False
        self.rejected("entry_exists")

    def test_candidate_fields_and_snapshot_drift_force_reaudit(self):
        original = copy.deepcopy(self.data)
        for field, value in (("source_url", self.record["source_url"] + "-other"),
                             ("revision", "c" * 40), ("business_categories", ["corporate-ma"]),
                             ("jurisdiction", {**self.record["jurisdiction"], "value": "other"}),
                             ("runtime_review", {**self.record["runtime_review"], "value": "other"})):
            with self.subTest(field=field):
                self.data = copy.deepcopy(original)
                self.record[field] = value
                self.rejected(field)
        self.data = copy.deepcopy(original)
        self.candidate["description"] += " Updated source claim."
        self.rejected("candidate changed; re-audit")

    def test_pending_authorization_cannot_be_laundered_as_clear(self):
        self.candidate.update(candidate_status="needs-evidence")
        self.candidate["authorization"]["status"] = "pending-verification"
        self.record["candidate_snapshot_sha256"] = fingerprint(self.candidate)
        self.record["p1_status"] = "blocked"
        self.record["blockers"] = [self.blocker()]
        self.rejected("unresolved candidate authorization cannot become clear")
        self.record["authorization_review"]["status"] = "missing-license"
        self.assertEqual(self.result(), (1, []))

    def test_currency_never_accepts_source_dates_or_claimed_review(self):
        original = copy.deepcopy(self.data)
        self.record["regulatory_currency"]["as_of"] = self.data["audited_at"]
        self.rejected("as_of")
        self.data = copy.deepcopy(original)
        self.record["regulatory_currency"].update(status="verified", as_of="2026-10-16",
                                                 evidence_urls=[self.record["source_url"]])
        self.rejected("regulatory_currency/status")
        # Even changing both manifests and recalculating the snapshot cannot turn
        # this P0 engineering audit into a professional approval channel.
        self.candidate["regulatory_currency"] = copy.deepcopy(self.record["regulatory_currency"])
        self.record["candidate_snapshot_sha256"] = fingerprint(self.candidate)
        self.rejected("regulatory_currency/status")
        self.data = copy.deepcopy(original)
        self.candidates = json.loads((FIXTURES / "candidates.json").read_text())
        self.record["professional_review"]["status"] = "approved"
        self.rejected("professional_review/status")

    def test_evidence_requires_pinned_observed_files_and_consistent_blob_claims(self):
        original = copy.deepcopy(self.data)
        for url in (self.record["source_url"].replace("/" + "a" * 40 + "/", "/main/"),
                    self.record["source_url"].replace("/example/", "/other/")):
            self.data = copy.deepcopy(original)
            self.record["audit_evidence"][0]["url"] = url
            self.rejected("evidence must pin original repository and revision")
        self.data = copy.deepcopy(original)
        self.record["audit_evidence"].append(copy.deepcopy(self.record["audit_evidence"][0]))
        self.rejected("duplicate evidence URL")
        self.data = copy.deepcopy(original)
        self.record["audit_evidence"][0]["blob_sha"] = None
        self.rejected("read files require a blob SHA")
        self.data = copy.deepcopy(original)
        self.record["audit_evidence"][0]["access"] = "not-found"
        self.rejected("missing paths and trees have no file blob SHA")
        self.data = copy.deepcopy(original)
        self.record["authorization_review"]["evidence_urls"] = ["https://example.com/unobserved"]
        self.rejected("must reference recorded audit evidence")

    def test_rejection_cannot_be_reopened_as_merely_blocked(self):
        self.candidate["candidate_status"] = "rejected"
        self.record["candidate_snapshot_sha256"] = fingerprint(self.candidate)
        self.record.update(p1_status="blocked", blockers=[self.blocker()])
        self.rejected("must remain rejected")
        self.record["p1_status"] = "rejected"
        self.assertEqual(self.result(), (1, []))

    def test_invalid_source_json_and_cli_errors_fail_closed(self):
        self.save()
        for filename in (self.path, self.candidates_path):
            for raw in ('{"records":', '{"records":[],"records":[]}',
                        '{"records":[NaN]}', '{"records":[Infinity]}'):
                with self.subTest(filename=filename, raw=raw):
                    self.save()
                    filename.write_text(raw)
                    result = subprocess.run([sys.executable, str(CLI), str(self.path),
                                             "--candidates", str(self.candidates_path)],
                                            capture_output=True, text=True, check=False)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn(str(filename), result.stderr)
                    self.assertIn("FAIL:", result.stderr)
        self.save()
        for filename in (self.path, self.candidates_path):
            self.save()
            filename.write_bytes(b"\xff")
            self.assertTrue(validate(self.path, self.candidates_path)[1])
            filename.unlink()
            self.assertTrue(validate(self.path, self.candidates_path)[1])

    def test_no_network_is_needed_for_validation(self):
        self.save()
        with patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            self.assertEqual(validate(self.path, self.candidates_path), (1, []))


if __name__ == "__main__":
    unittest.main()
