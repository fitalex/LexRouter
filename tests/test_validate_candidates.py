"""Offline CLI contract tests; all negative mutations use synthetic fixtures."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "validate_candidates.py"
FIXTURES = ROOT / "tests" / "fixtures" / "candidates"
VALID = FIXTURES / "valid.json"


class CandidateCLITests(unittest.TestCase):
    def run_cli(self, *paths, cli=CLI):
        return subprocess.run([sys.executable, str(cli), *(str(p) for p in paths)],
                              capture_output=True, text=True, check=False, cwd=ROOT)

    def assert_rejected(self, path, field):
        result = self.run_cli(path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(str(path), result.stderr)
        self.assertIn(field, result.stderr)
        self.assertIn("FAIL:", result.stderr)

    def test_fixed_valid_fixture(self):
        result = self.run_cli(VALID)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS: 1 candidate record(s)", result.stdout)
        self.assertIn("no network or legal/license verification", result.stdout)

    def test_actual_manifest_and_default_path(self):
        for paths in ((), (ROOT / "data" / "discovery" / "candidates.json",)):
            with self.subTest(paths=paths):
                result = self.run_cli(*paths)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_fixed_negative_fixtures(self):
        for name, pointer in (
            ("missing-source", "/candidates/0/source_url"),
            ("duplicate-id", "/candidates/1/candidate_id: duplicate candidate ID"),
            ("illegal-status", "/candidates/0/candidate_status"),
            ("missing-authorization", "/candidates/0/authorization"),
            ("missing-authorization-status", "/candidates/0/authorization/status"),
            ("missing-regulatory-currency", "/candidates/0/regulatory_currency"),
            ("missing-regulatory-status", "/candidates/0/regulatory_currency/status"),
        ):
            with self.subTest(name=name):
                self.assert_rejected(FIXTURES / "invalid" / (name + ".json"), pointer)

    def test_all_fields_are_required_including_nested_fields(self):
        original = json.loads(VALID.read_text())
        candidate = original["candidates"][0]
        paths = [(key,) for key in candidate]
        paths += [(key, child) for key, value in candidate.items()
                  if isinstance(value, dict) for child in value]
        paths += [("format_version",), ("candidates",)]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidate.json"
            for parts in paths:
                with self.subTest(parts=parts):
                    data = json.loads(VALID.read_text())
                    target = data if parts[0] in ("format_version", "candidates") else data["candidates"][0]
                    for part in parts[:-1]:
                        target = target[part]
                    del target[parts[-1]]
                    path.write_text(json.dumps(data))
                    self.assert_rejected(path, "/" + "/".join(parts))

    def test_invalid_urls_types_enums_and_dates(self):
        cases = [
            (("source_url",), url) for url in
            ("", "not-a-url", "http://example.com/skill", "https://", "https://example.com/a b")
        ] + [
            (("candidate_id",), "Invalid ID"), (("name",), "  "),
            (("description",), None), (("business_categories",), []),
            (("business_categories",), ["unknown"]),
            (("business_categories",), ["contract-review", "contract-review"]),
            (("runtime",), "unknown"), (("jurisdiction", "status"), "guessed"),
            (("jurisdiction", "value"), "CN"),
            (("source_verification", "status"), "url-format-only"),
            (("source_verification", "checked_at"), "2026-02-30"),
            (("source_verification", "checked_at"), "2026-2-01"),
            (("source_verification", "evidence_urls"), []),
            (("authorization", "status"), "unknown"),
            (("authorization", "status"), None),
            (("authorization", "license"), ""),
            (("authorization", "evidence_urls"), ["not-a-url"]),
            (("regulatory_currency", "status"), "unknown"),
            (("regulatory_currency", "status"), None),
            (("regulatory_currency", "as_of"), "2026-10-16"),
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidate.json"
            for parts, value in cases:
                with self.subTest(parts=parts, value=value):
                    data = json.loads(VALID.read_text())
                    target = data["candidates"][0]
                    for part in parts[:-1]:
                        target = target[part]
                    target[parts[-1]] = value
                    path.write_text(json.dumps(data))
                    self.assert_rejected(path, "/candidates/0/" + "/".join(parts))

    def test_verified_currency_requires_date_and_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidate.json"
            data = json.loads(VALID.read_text())
            currency = data["candidates"][0]["regulatory_currency"]
            currency["status"] = "verified"
            path.write_text(json.dumps(data))
            self.assert_rejected(path, "/regulatory_currency/as_of")
            currency["as_of"] = "2024-02-29"
            path.write_text(json.dumps(data))
            self.assert_rejected(path, "/regulatory_currency/evidence_urls")
            currency["evidence_urls"] = ["https://example.com/synthetic-review"]
            path.write_text(json.dumps(data))
            result = self.run_cli(path)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_candidate_requires_source_license_and_jurisdiction_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidate.json"
            data = json.loads(VALID.read_text())
            candidate = data["candidates"][0]
            candidate["candidate_status"] = "candidate"
            path.write_text(json.dumps(data))
            for pointer in ("/source_verification/status", "/authorization/status",
                            "/jurisdiction/value", "/jurisdiction/status"):
                self.assert_rejected(path, pointer)
            candidate["source_verification"]["status"] = "verified-public"
            candidate["authorization"]["status"] = "verified"
            candidate["jurisdiction"].update(value="CN-Mainland", status="source-declared")
            path.write_text(json.dumps(data))
            self.assertEqual(self.run_cli(path).returncode, 0)

    def test_not_permitted_requires_rejection(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidate.json"
            data = json.loads(VALID.read_text())
            candidate = data["candidates"][0]
            candidate["authorization"]["status"] = "not-permitted"
            path.write_text(json.dumps(data))
            self.assert_rejected(path, "/candidate_status")
            candidate["candidate_status"] = "rejected"
            path.write_text(json.dumps(data))
            self.assertEqual(self.run_cli(path).returncode, 0)

    def test_rejects_nonobjects_and_extra_fields(self):
        original = json.loads(VALID.read_text())
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidate.json"
            for value in ([], None, {**original, "extra": True},
                          {"format_version": 1, "candidates": [None]},
                          {"format_version": 1, "candidates": "wrong"},
                          {"format_version": True, "candidates": []}):
                with self.subTest(value=value):
                    path.write_text(json.dumps(value))
                    self.assert_rejected(path, "/")
            original["candidates"][0]["regulatory_as_of"] = "2026-10-16"
            path.write_text(json.dumps(original))
            self.assert_rejected(path, "regulatory_as_of")

    def test_rejects_malformed_duplicate_keys_and_non_json_constants(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidate.json"
            for content, expected in (
                ('{"candidates":', "line 1, column"),
                ('{"format_version":1,"format_version":1,"candidates":[]}', "duplicate JSON object key"),
                ('{"candidates":[NaN]}', "non-JSON constant"),
                ('{"candidates":[Infinity]}', "non-JSON constant"),
            ):
                with self.subTest(content=content):
                    path.write_text(content)
                    self.assert_rejected(path, expected)

    def test_missing_unreadable_paths_and_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.json"
            self.assert_rejected(path, "cannot read UTF-8 JSON")
            self.assert_rejected(Path(folder), "cannot read UTF-8 JSON")
            path.write_bytes(b"\xff")
            self.assert_rejected(path, "cannot read UTF-8 JSON")

    def test_empty_manifest_reports_zero(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty.json"
            path.write_text('{"format_version":1,"candidates":[]}')
            result = self.run_cli(path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("0 candidate record(s)", result.stdout)
            self.assertIn("does not demonstrate discovery coverage", result.stdout)

    def test_candidate_and_formal_contracts_remain_separate(self):
        result = self.run_cli(VALID, cli=ROOT / "scripts" / "validate_skills.py")
        self.assertEqual(result.returncode, 1)
        self.assertIn("/regulatory_as_of", result.stderr)
        self.assert_rejected(ROOT / "tests" / "fixtures" / "valid" / "metadata.json", "/candidates")
        result = self.run_cli(ROOT / "tests" / "fixtures" / "valid" / "metadata.json",
                              cli=ROOT / "scripts" / "validate_skills.py")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
