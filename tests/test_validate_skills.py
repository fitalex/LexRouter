"""Exercise the actual CLI and its public metadata contract with synthetic data."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "validate_skills.py"
FIXTURES = ROOT / "tests" / "fixtures"
VALID = FIXTURES / "valid" / "metadata.json"


class MetadataCLITests(unittest.TestCase):
    def run_cli(self, *paths):
        return subprocess.run([sys.executable, str(CLI), *(str(p) for p in paths)],
                              capture_output=True, text=True, check=False)

    def assert_rejected(self, path, field):
        result = self.run_cli(path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(str(path), result.stderr)
        self.assertIn(field, result.stderr)
        self.assertIn("FAIL:", result.stderr)

    def test_fixed_valid_file_and_directory(self):
        for path in (VALID, VALID.parent):
            with self.subTest(path=path):
                result = self.run_cli(path)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("PASS: 1 metadata file(s) validated.", result.stdout)

    def test_fixed_missing_required_fields(self):
        for name, field in (
            ("missing-jurisdiction.json", "/jurisdiction"),
            ("missing-business-categories.json", "/business_categories"),
            ("missing-regulatory-as-of.json", "/regulatory_as_of"),
        ):
            with self.subTest(field=field):
                self.assert_rejected(FIXTURES / "invalid" / name, field)

    def test_fixed_wrong_type(self):
        self.assert_rejected(FIXTURES / "invalid" / "wrong-type.json", "/business_categories")

    def test_invalid_directory_reports_each_file(self):
        result = self.run_cli(FIXTURES / "invalid")
        self.assertEqual(result.returncode, 1)
        for path in (FIXTURES / "invalid").glob("*.json"):
            self.assertIn(str(path), result.stderr)
        self.assertIn("across 4 metadata file(s)", result.stderr)

    def test_rejects_invalid_dates_enums_and_shapes(self):
        cases = [
            ("regulatory_as_of", "unknown"),
            ("regulatory_as_of", "2026-02-30"),
            ("regulatory_as_of", "2026-2-01"),
            ("regulatory_as_of", None),
            ("jurisdiction", "unknown"),
            ("business_categories", []),
            ("business_categories", ["unknown"]),
            ("business_categories", ["contract-review", "contract-review"]),
            ("runtime", "unknown"),
            ("source_url", "not-a-url"),
            ("source_url", "http://example.com/skill"),
            ("name", "   "),
            ("description", ""),
            ("id", "Invalid ID"),
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "metadata.json"
            for field, value in cases:
                with self.subTest(field=field, value=value):
                    data = json.loads(VALID.read_text(encoding="utf-8"))
                    data[field] = value
                    path.write_text(json.dumps(data), encoding="utf-8")
                    self.assert_rejected(path, "/" + field)

    def test_rejects_extra_fields_and_non_object(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "metadata.json"
            data = json.loads(VALID.read_text(encoding="utf-8"))
            data["unexpected"] = True
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assert_rejected(path, "unexpected")
            path.write_text("[]", encoding="utf-8")
            self.assert_rejected(path, "/")

    def test_duplicate_ids_across_nested_files(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            nested = base / "nested"
            nested.mkdir()
            (base / "first.json").write_bytes(VALID.read_bytes())
            second = nested / "second.json"
            second.write_bytes(VALID.read_bytes())
            result = self.run_cli(base)
            self.assertEqual(result.returncode, 1)
            self.assertIn(str(second), result.stderr)
            self.assertIn("/id: duplicate id", result.stderr)
            self.assertIn(str(base / "first.json"), result.stderr)

    def test_overlapping_input_paths_are_deduplicated(self):
        result = self.run_cli(VALID, VALID.parent)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS: 1 metadata file(s)", result.stdout)

    def test_multiple_distinct_files_and_uppercase_extension(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "second.JSON"
            data = json.loads(VALID.read_text(encoding="utf-8"))
            data["id"] = "synthetic-second"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_cli(VALID, folder)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("PASS: 2 metadata file(s)", result.stdout)

    def test_missing_path_non_json_malformed_and_invalid_encoding(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            self.assert_rejected(base / "missing.json", "path does not exist")
            text = base / "metadata.txt"
            text.write_text("{}", encoding="utf-8")
            self.assert_rejected(text, "expected a JSON")
            malformed = base / "malformed.json"
            malformed.write_text('{"id":', encoding="utf-8")
            self.assert_rejected(malformed, "line 1, column")
            malformed.write_bytes(b"\xff")
            self.assert_rejected(malformed, "cannot read UTF-8 JSON")

    def test_empty_directory_is_explicit(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_cli(folder)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("0 metadata file(s)", result.stdout)
            self.assertIn("Run fixture tests", result.stdout)

    def test_valid_leap_day(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "metadata.json"
            data = json.loads(VALID.read_text(encoding="utf-8"))
            data["regulatory_as_of"] = "2024-02-29"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_cli(path)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
