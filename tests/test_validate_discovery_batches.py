"""Synthetic cross-batch regressions; never fetch or execute third-party skills."""

from copy import deepcopy
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
from validate_discovery_batches import source_identity, summary, validate_batches


class DiscoveryBatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.record = json.loads((ROOT / "tests/fixtures/candidates/valid.json").read_text())["candidates"][0]
        self.record["source_verification"]["revision"] = "a" * 40
        self.record["source_url"] = "https://github.com/example/synthetic/blob/" + "a" * 40 + "/one/SKILL.md"
        self.record["source_verification"]["evidence_urls"] = [self.record["source_url"]]

    def write(self, name, records):
        path = self.folder / name
        path.write_text(json.dumps({"format_version": 1, "candidates": records}), encoding="utf-8")
        return path

    def second(self):
        other = deepcopy(self.record)
        other["candidate_id"] = "synthetic-second"
        other["source_url"] = other["source_url"].replace("/one/", "/two/")
        other["source_verification"]["evidence_urls"] = [other["source_url"]]
        return other

    def test_independent_entries_same_suite_and_offline_counts(self):
        paths = [self.write("old.json", [self.record]), self.write("new.json", [self.second()])]
        with patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            records, errors = validate_batches(paths)
        self.assertEqual(errors, [])
        self.assertEqual(summary(records)["records"], 2)
        self.assertEqual(sum(summary(records)["candidate_status"].values()), 2)
        self.assertEqual(summary(records)["business_categories"],
                         {c: 2 for c in self.record["business_categories"]})

    def test_duplicate_id_with_different_source(self):
        other = self.second()
        other["candidate_id"] = self.record["candidate_id"]
        _, errors = validate_batches([self.write("old.json", [self.record]), self.write("new.json", [other])])
        self.assertTrue(any("/candidates/0/candidate_id: duplicate" in e and "old.json" in e for e in errors))

    def test_same_source_across_commits_hosts_and_runtimes(self):
        urls = [
            "https://github.com/EXAMPLE/SYNTHETIC/blob/" + "b" * 40 + "/one/SKILL.md?plain=1#L1",
            "https://raw.githubusercontent.com/example/synthetic/" + "b" * 40 + "/one/SKILL.md",
            "https://www.github.com/example/synthetic/raw/" + "b" * 40 + "/one/%53KILL.md",
        ]
        for url in urls:
            with self.subTest(url=url):
                other = self.second()
                other.update(source_url=url, runtime="other")
                other["source_verification"].update(revision="b" * 40, evidence_urls=[url])
                _, errors = validate_batches([self.write("old.json", [self.record]), self.write("new.json", [other])])
                self.assertTrue(any("duplicate source entry" in e for e in errors), errors)

    def test_path_case_and_different_files_are_distinct(self):
        url = self.record["source_url"]
        self.assertNotEqual(source_identity(url), source_identity(url.replace("SKILL.md", "skill.md")))
        self.assertNotEqual(source_identity(url), source_identity(self.second()["source_url"]))

    def test_pin_and_evidence_errors(self):
        for change, field in [
            (lambda r: r["source_verification"].update(revision="main"), "revision"),
            (lambda r: r.update(source_url=r["source_url"].replace("a" * 40, "main")), "source_url"),
            (lambda r: r["source_verification"].update(evidence_urls=["https://example.com/other"]), "evidence_urls"),
        ]:
            with self.subTest(field=field):
                record = deepcopy(self.record)
                change(record)
                _, errors = validate_batches([self.write("bad.json", [record])])
                self.assertTrue(any(field in e for e in errors), errors)

    def test_repeated_file_does_not_inflate_count(self):
        path = self.write("one.json", [self.record])
        records, errors = validate_batches([path, path])
        self.assertEqual(len(records), 1)
        self.assertIn("repeated input manifest", errors[0])

    def test_bad_manifest_reuses_contract_and_excludes_records(self):
        record = deepcopy(self.record)
        del record["authorization"]
        records, errors = validate_batches([self.write("bad.json", [record])])
        self.assertEqual(records, [])
        self.assertTrue(any("authorization" in e for e in errors))

    def test_unreadable_and_malformed_json(self):
        path = self.folder / "bad.json"
        for content in [b'{"format_version":1,"format_version":1}', b'{', b'\xff', b'{"candidates":NaN}']:
            path.write_bytes(content)
            _, errors = validate_batches([path])
            self.assertTrue(errors)
        _, errors = validate_batches([self.folder / "missing.json"])
        self.assertTrue(errors)

    def test_cli_success_failure_and_argument_exit_codes(self):
        cli = ROOT / "scripts/validate_discovery_batches.py"
        good = self.write("good.json", [self.record])
        duplicate = self.write("duplicate.json", [self.record])
        for args, code, message in [([good], 0, "semantic capability duplicates require manual review"),
                                    ([good, duplicate], 1, "no deduplicated count certified"),
                                    ([], 2, "required")]:
            result = subprocess.run([sys.executable, str(cli), *map(str, args)], capture_output=True, text=True)
            self.assertEqual(result.returncode, code, result.stdout + result.stderr)
            self.assertIn(message, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
