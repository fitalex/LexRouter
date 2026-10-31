"""Offline Discovery adapter tests; all fixtures are synthetic.

No test opens a socket, contacts a search/fetch API, executes a third-party
Skill, or writes into ``data/discovery/`` or ``skills/``.
"""

from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timezone
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from discovery import (  # noqa: E402
    DiscoveryAdapter,
    FetchAdapter,
    FetchStatus,
    FixtureSourceStore,
    NormalizationError,
    PinnedRef,
    SearchAdapter,
    SearchHit,
    SearchStatus,
    dedupe_hits,
    normalize,
    source_identity,
)
from validate_candidates import validate as validate_candidate_manifest  # noqa: E402
from validate_discovery_batches import (  # noqa: E402
    source_identity as validator_source_identity,
    validate_batches,
)
from validate_skills import validate as validate_formal_metadata  # noqa: E402
import discovery_offline as offline_cli  # noqa: E402


FIXTURES = ROOT / "tests" / "fixtures" / "discovery"
SEARCH_FIXTURE = FIXTURES / "search_responses.json"
SOURCE_FIXTURE = FIXTURES / "sources.json"
CLI = ROOT / "scripts" / "discovery_offline.py"

SHA_A = "a" * 40
SHA_B = "b" * 40
SHA_C = "c" * 40
SHA_D = "d" * 40

ALLOWED_URL = f"https://github.com/synthetic-labs/contract-review-skill/blob/{SHA_A}/SKILL.md"
RESTRICTED_URL = f"https://github.com/synthetic-labs/restricted-legal-index/blob/{SHA_C}/SKILL.md"


def fixed_now():
    return datetime(2026, 10, 31, 10, 0, 0, tzinfo=timezone.utc)


def make_adapter():
    return DiscoveryAdapter.from_fixtures(SEARCH_FIXTURE, SOURCE_FIXTURE, now=fixed_now)


def source_record():
    return deepcopy(json.loads(SOURCE_FIXTURE.read_text(encoding="utf-8"))["sources"][0])


class SingleRecordStore:
    """Return one mutated synthetic record for negative pin tests."""

    def __init__(self, record):
        self.record = record

    def get(self, source_id):
        return self.record if source_id == self.record["source_id"] else None


def make_hit(**changes):
    values = {
        "hit_id": "synthetic-hit",
        "source_id": "synthetic-contract-review",
        "title": "Synthetic contract review workflow",
        "url": ALLOWED_URL,
        "snippet": "Synthetic snippet for offline tests.",
        "retrieved_at": "2026-10-30",
        "provider": "synthetic-test",
        "rank": 1,
        "revision": SHA_A,
        "business_categories": ("contract-review",),
    }
    values.update(changes)
    return SearchHit(**values)


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.adapter = make_adapter()

    def test_normal_response_is_standardized(self):
        result = self.adapter.search("合成合同审查")
        self.assertIs(result.status, SearchStatus.OK)
        self.assertEqual(len(result.hits), 3)
        self.assertEqual(result.provider, "synthetic-discovery-search")
        first = result.hits[0]
        self.assertEqual(first.source_id, "synthetic-contract-review")
        self.assertEqual(first.url, ALLOWED_URL)
        self.assertEqual(first.revision, SHA_A)
        self.assertEqual(first.business_categories, ("contract-review",))
        self.assertEqual(first.rank, 1)
        self.assertEqual(first.retrieved_at, "2026-10-30")

    def test_empty_result_is_not_an_error(self):
        result = self.adapter.search("空结果")
        self.assertIs(result.status, SearchStatus.EMPTY)
        self.assertEqual(result.hits, ())
        self.assertIsNone(result.error)

    def test_provider_error_is_preserved(self):
        result = self.adapter.search("网络错误")
        self.assertIs(result.status, SearchStatus.ERROR)
        self.assertEqual(result.hits, ())
        self.assertEqual(result.error.code, "timeout")
        self.assertTrue(result.error.retryable)

    def test_os_error_from_transport_becomes_error_status(self):
        class FailingTransport:
            provider = "synthetic-failing"

            def request(self, query, limit):
                raise TimeoutError("synthetic socket timeout")

        result = SearchAdapter(FailingTransport()).search("anything")
        self.assertIs(result.status, SearchStatus.ERROR)
        self.assertEqual(result.error.code, "transport-error")
        self.assertTrue(result.error.retryable)

    def test_malformed_payload_is_rejected(self):
        result = self.adapter.search("结构错误")
        self.assertIs(result.status, SearchStatus.ERROR)
        self.assertEqual(result.error.code, "invalid-response")

    def test_unknown_query_and_bad_arguments(self):
        for query, code in [
            ("", "invalid-query"),
            (None, "invalid-query"),
            ("未配置查询", "fixture-not-found"),
        ]:
            with self.subTest(query=query):
                result = self.adapter.search(query)
                self.assertIs(result.status, SearchStatus.ERROR)
                self.assertEqual(result.error.code, code)
        self.assertEqual(self.adapter.search("空结果", limit=0).error.code, "invalid-limit")

    def test_missing_hit_fields_survive_for_normalization(self):
        result = self.adapter.search("缺失字段")
        self.assertIs(result.status, SearchStatus.OK)
        self.assertEqual(len(result.hits), 1)
        self.assertEqual(result.hits[0].title, "")
        with self.assertRaises(NormalizationError) as raised:
            normalize(result.hits[0])
        self.assertEqual(raised.exception.field, "title")


class FetchTests(unittest.TestCase):
    def setUp(self):
        self.adapter = make_adapter()

    def test_pinned_read_preserves_version_and_evidence(self):
        ref = PinnedRef("synthetic-contract-review", ALLOWED_URL, SHA_A)
        snapshot = self.adapter.fetch_pinned(ref)
        self.assertIs(snapshot.status, FetchStatus.OK)
        self.assertEqual(snapshot.revision, SHA_A)
        self.assertEqual(snapshot.retrieved_at, "2026-10-30")
        self.assertEqual(snapshot.license, "MIT")
        self.assertIn(ALLOWED_URL, snapshot.evidence_urls)
        self.assertIn("SYNTHETIC-ALLOWED-CONTENT", snapshot.content or "")

    def test_stored_url_must_be_pinned_to_its_recorded_revision(self):
        record = source_record()
        record["url"] = record["url"].replace(SHA_A, SHA_B)
        snapshot = FetchAdapter(SingleRecordStore(record)).fetch_pinned(
            PinnedRef(record["source_id"], ALLOWED_URL, SHA_A)
        )
        self.assertIs(snapshot.status, FetchStatus.INVALID_SOURCE)
        self.assertIsNone(snapshot.content)

    def test_stored_url_must_not_be_a_branch(self):
        record = source_record()
        record["url"] = (
            "https://github.com/synthetic-labs/contract-review-skill/blob/main/SKILL.md"
        )
        snapshot = FetchAdapter(SingleRecordStore(record)).fetch_pinned(
            PinnedRef(record["source_id"], ALLOWED_URL, SHA_A)
        )
        self.assertIs(snapshot.status, FetchStatus.INVALID_SOURCE)
        self.assertIsNone(snapshot.content)

    def test_exact_stored_pin_is_accepted(self):
        record = source_record()
        snapshot = FetchAdapter(SingleRecordStore(record)).fetch_pinned(
            PinnedRef(record["source_id"], ALLOWED_URL, SHA_A)
        )
        self.assertIs(snapshot.status, FetchStatus.OK)
        self.assertIn("SYNTHETIC-ALLOWED-CONTENT", snapshot.content or "")

    def test_invalid_stored_pin_never_verifies_or_leaks_content(self):
        record = source_record()
        record["url"] = record["url"].replace(SHA_A, SHA_B)
        snapshot = FetchAdapter(SingleRecordStore(record)).fetch_pinned(
            PinnedRef(record["source_id"], ALLOWED_URL, SHA_A)
        )
        self.assertIs(snapshot.status, FetchStatus.INVALID_SOURCE)
        self.assertIsNone(snapshot.content)
        candidate = normalize(make_hit(), snapshot)
        self.assertNotEqual(candidate["source_verification"]["status"], "verified-public")
        self.assertEqual(candidate["candidate_status"], "needs-evidence")

    def test_revision_mismatch_is_explicit_and_has_no_content(self):
        url = f"https://github.com/synthetic-labs/contract-review-skill/blob/{SHA_B}/SKILL.md"
        snapshot = self.adapter.fetch_pinned(
            PinnedRef("synthetic-contract-review", url, SHA_B)
        )
        self.assertIs(snapshot.status, FetchStatus.REVISION_MISMATCH)
        self.assertIsNone(snapshot.content)
        self.assertIsNone(snapshot.revision)
        self.assertIn("revision", snapshot.notes)

    def test_unpinned_or_non_github_ref_is_invalid(self):
        for ref in [
            PinnedRef(
                "synthetic-contract-review",
                "https://github.com/synthetic-labs/contract-review-skill/blob/main/SKILL.md",
                SHA_A,
            ),
            PinnedRef(
                "synthetic-contract-review",
                f"https://example.com/skill/{SHA_A}/SKILL.md",
                SHA_A,
            ),
            PinnedRef("synthetic-contract-review", ALLOWED_URL, "main"),
        ]:
            with self.subTest(ref=ref):
                snapshot = self.adapter.fetch_pinned(ref)
                self.assertIs(snapshot.status, FetchStatus.INVALID_REF)
                self.assertIsNone(snapshot.content)

    def test_unknown_id_and_source_mismatch(self):
        missing = self.adapter.fetch_pinned(PinnedRef("synthetic-missing", ALLOWED_URL, SHA_A))
        self.assertIs(missing.status, FetchStatus.NOT_FOUND)
        mismatched = self.adapter.fetch_pinned(
            PinnedRef("synthetic-contract-review", RESTRICTED_URL, SHA_C)
        )
        self.assertIs(mismatched.status, FetchStatus.SOURCE_MISMATCH)
        self.assertIsNone(mismatched.content)

    def test_reference_only_full_text_is_withheld(self):
        snapshot = self.adapter.fetch_pinned(
            PinnedRef("synthetic-restricted-index", RESTRICTED_URL, SHA_C)
        )
        self.assertIs(snapshot.status, FetchStatus.METADATA_ONLY)
        self.assertIsNone(snapshot.content)
        self.assertIn("withheld", snapshot.notes)
        self.assertNotIn("DO-NOT-COPY-SYNTHETIC-MARKER", snapshot.notes)

    def test_store_read_error_is_preserved(self):
        class BrokenStore:
            def get(self, source_id):
                raise OSError("synthetic store failure")

        snapshot = FetchAdapter(BrokenStore()).fetch_pinned(
            PinnedRef("x", ALLOWED_URL, SHA_A)
        )
        self.assertIs(snapshot.status, FetchStatus.TRANSPORT_ERROR)
        self.assertIsNone(snapshot.content)

    def test_store_rejects_duplicate_source_ids(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sources.json"
            path.write_text(json.dumps({
                "fixture_version": 1,
                "sources": [{"source_id": "same"}, {"source_id": "same"}],
            }))
            with self.assertRaises(ValueError):
                FixtureSourceStore(path)


class NormalizeTests(unittest.TestCase):
    def setUp(self):
        self.adapter = make_adapter()
        result = self.adapter.search("合成合同审查")
        self.allowed_hit = result.hits[0]
        self.restricted_hit = result.hits[2]
        self.allowed_snapshot = self.adapter.fetch_pinned(PinnedRef.from_hit(self.allowed_hit))
        self.restricted_snapshot = self.adapter.fetch_pinned(PinnedRef.from_hit(self.restricted_hit))

    def test_fetched_hits_pass_the_existing_candidate_validator(self):
        candidates = [
            normalize(self.allowed_hit, self.allowed_snapshot),
            normalize(self.restricted_hit, self.restricted_snapshot),
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidates.json"
            path.write_text(json.dumps({"format_version": 1, "candidates": candidates}))
            count, errors = validate_candidate_manifest(path)
        self.assertEqual((count, errors), (2, []))

    def test_candidate_status_is_derived_from_evidence(self):
        allowed = normalize(self.allowed_hit, self.allowed_snapshot)
        restricted = normalize(self.restricted_hit, self.restricted_snapshot)
        self.assertEqual(allowed["candidate_status"], "candidate")
        self.assertEqual(restricted["candidate_status"], "needs-evidence")

        rejected = normalize(
            self.allowed_hit,
            replace(self.allowed_snapshot, authorization_status="not-permitted"),
        )
        self.assertEqual(rejected["candidate_status"], "rejected")

    def test_missing_required_fields_raise_with_actionable_field(self):
        cases = [
            (make_hit(title=""), "title"),
            (make_hit(url=""), "url"),
            (make_hit(url="http://example.com/skill"), "url"),
            (make_hit(retrieved_at=""), "retrieved_at"),
            (make_hit(retrieved_at="2026-02-30"), "retrieved_at"),
            (make_hit(business_categories=()), "business_categories"),
            (make_hit(business_categories=("unknown",)), "business_categories"),
        ]
        for hit, field in cases:
            with self.subTest(field=field):
                with self.assertRaises(NormalizationError) as raised:
                    normalize(hit)
                self.assertEqual(raised.exception.field, field)

    def test_missing_snippet_uses_an_original_fallback(self):
        candidate = normalize(make_hit(snippet=""))
        self.assertIn("未读取", candidate["description"])
        self.assertNotEqual(candidate["description"], candidate["name"])

    def test_search_only_hit_is_unverified_and_not_a_candidate(self):
        candidate = normalize(self.allowed_hit)
        self.assertEqual(candidate["source_verification"]["status"], "unverified")
        self.assertEqual(candidate["authorization"]["status"], "pending-verification")
        self.assertEqual(candidate["candidate_status"], "needs-evidence")
        self.assertIn("仅搜索命中", candidate["source_verification"]["notes"])

    def test_unknown_states_are_explicit_and_not_upgraded(self):
        snapshot = replace(
            self.allowed_snapshot,
            authorization_status="approved-by-magic",
            license="",
            jurisdiction={
                "value": "Mars",
                "status": "assumed",
                "evidence_url": "http://insecure.example/readme",
                "notes": "",
            },
            runtime="mystery-runtime",
        )
        candidate = normalize(replace(self.allowed_hit, runtime=None), snapshot)
        self.assertEqual(candidate["authorization"]["status"], "pending-verification")
        self.assertEqual(candidate["authorization"]["license"], "not-identified")
        self.assertEqual(candidate["jurisdiction"]["value"], "unknown")
        self.assertEqual(candidate["jurisdiction"]["status"], "pending-verification")
        self.assertEqual(candidate["jurisdiction"]["evidence_url"], ALLOWED_URL)
        self.assertEqual(candidate["runtime"], "other")
        self.assertEqual(candidate["candidate_status"], "needs-evidence")

    def test_missing_jurisdiction_evidence_is_not_source_declared(self):
        for evidence in ("", "http://insecure.example/readme"):
            with self.subTest(evidence=evidence):
                snapshot = replace(self.allowed_snapshot, jurisdiction={
                    "value": "CN-Mainland",
                    "status": "source-declared",
                    "evidence_url": evidence,
                    "notes": "",
                })
                candidate = normalize(self.allowed_hit, snapshot)
                self.assertEqual(candidate["jurisdiction"]["value"], "CN-Mainland")
                self.assertEqual(
                    candidate["jurisdiction"]["status"], "pending-verification"
                )
                self.assertTrue(
                    candidate["jurisdiction"]["evidence_url"].endswith("/SKILL.md")
                )
                self.assertEqual(candidate["candidate_status"], "needs-evidence")

    def test_verified_states_require_evidence_and_never_claim_legal_review(self):
        no_license = replace(
            self.allowed_snapshot,
            authorization_status="verified",
            license="not-identified",
            authorization_evidence_urls=(),
            jurisdiction={
                "value": "CN-Mainland",
                "status": "verified",
                "evidence_url": ALLOWED_URL,
                "notes": "",
            },
        )
        candidate = normalize(self.allowed_hit, no_license)
        self.assertEqual(candidate["authorization"]["status"], "pending-verification")
        self.assertEqual(candidate["jurisdiction"]["status"], "source-declared")
        self.assertIn("不执行法律专业复核", candidate["jurisdiction"]["notes"])

    def test_regulatory_currency_is_never_filled_in(self):
        for candidate in [
            normalize(self.allowed_hit, self.allowed_snapshot),
            normalize(self.restricted_hit, self.restricted_snapshot),
            normalize(self.allowed_hit),
        ]:
            with self.subTest(candidate=candidate["candidate_id"]):
                currency = candidate["regulatory_currency"]
                self.assertEqual(currency["status"], "not-checked")
                self.assertIsNone(currency["as_of"])
                self.assertEqual(currency["evidence_urls"], [])

    def test_full_text_is_never_copied_into_a_candidate(self):
        candidates = [
            normalize(self.allowed_hit, self.allowed_snapshot),
            normalize(self.restricted_hit, self.restricted_snapshot),
        ]
        serialized = json.dumps({"format_version": 1, "candidates": candidates})
        self.assertNotIn("DO-NOT-COPY-SYNTHETIC-MARKER", serialized)
        self.assertNotIn("SYNTHETIC-ALLOWED-CONTENT", serialized)
        for candidate in candidates:
            self.assertNotIn("content", candidate)

    def test_snapshot_for_a_different_entry_is_rejected(self):
        with self.assertRaises(NormalizationError) as raised:
            normalize(self.allowed_hit, self.restricted_snapshot)
        self.assertEqual(raised.exception.field, "source_id")

    def test_candidate_has_exactly_the_candidate_contract_fields(self):
        candidate = normalize(self.allowed_hit, self.allowed_snapshot)
        self.assertEqual(set(candidate), {
            "candidate_id", "name", "description", "source_url", "maintainer",
            "business_categories", "jurisdiction", "runtime", "runtime_evidence",
            "source_verification", "authorization", "regulatory_currency",
            "candidate_status", "evidence_notes",
        })


class DedupTests(unittest.TestCase):
    def test_source_identity_matches_the_repository_validator(self):
        urls = [
            f"https://github.com/EXAMPLE/SYNTHETIC/blob/{SHA_B}/one/SKILL.md?plain=1#L1",
            f"https://raw.githubusercontent.com/example/synthetic/{SHA_B}/one/SKILL.md",
            f"https://www.github.com/example/synthetic/raw/{SHA_B}/one/%53KILL.md",
            f"https://github.com/example/synthetic/blob/{SHA_C}/two/SKILL.md",
            "https://example.com/one",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(source_identity(url), validator_source_identity(url))

    def test_same_entry_across_hosts_revisions_and_encoding_is_deduped(self):
        base = make_hit()
        mirror = replace(
            base,
            hit_id="mirror",
            url=f"https://raw.githubusercontent.com/synthetic-labs/contract-review-skill/{SHA_B}/SKILL.md",
            revision=SHA_B,
        )
        other_file = replace(
            base,
            hit_id="readme",
            url=f"https://github.com/synthetic-labs/contract-review-skill/blob/{SHA_A}/README.md",
        )
        unique, duplicates = dedupe_hits([base, mirror, other_file])
        self.assertEqual(len(unique), 2)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0].first_hit, base)
        self.assertEqual(duplicates[0].hit, mirror)

    def test_malformed_url_does_not_crash_deduplication(self):
        unique, duplicates = dedupe_hits([make_hit(url="https://[::1")])
        self.assertEqual(len(unique), 1)
        self.assertEqual(duplicates, ())

    def test_pipeline_dedupes_the_fixture_mirror(self):
        run = make_adapter().collect("合成合同审查")
        self.assertEqual(len(run.duplicates), 1)
        self.assertEqual(len(run.candidates), 2)


class PipelineAndSchemaTests(unittest.TestCase):
    def test_main_run_produces_contract_valid_candidates(self):
        run = make_adapter().collect("合成合同审查")
        self.assertEqual(run.search.status, SearchStatus.OK)
        self.assertEqual(len(run.candidates), 2)
        self.assertEqual(run.failures, ())
        self.assertEqual(run.content_withheld, 1)
        statuses = sorted(candidate["candidate_status"] for candidate in run.candidates)
        self.assertEqual(statuses, ["candidate", "needs-evidence"])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidates.json"
            path.write_text(json.dumps(run.manifest()))
            self.assertEqual(validate_candidate_manifest(path), (2, []))

    def test_main_run_passes_cross_batch_pin_and_duplicate_checks(self):
        run = make_adapter().collect("合成合同审查")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidates.json"
            path.write_text(json.dumps(run.manifest()))
            records, errors = validate_batches([path])
        self.assertEqual(errors, [])
        self.assertEqual(len(records), 2)

    def test_empty_run_reports_zero_without_failure(self):
        run = make_adapter().collect("空结果")
        self.assertEqual(run.search.status, SearchStatus.EMPTY)
        self.assertEqual(run.candidates, ())
        self.assertEqual(run.failures, ())
        audit = run.audit()
        self.assertEqual(audit["candidates"], 0)
        self.assertEqual(audit["search"]["status"], "empty")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidates.json"
            path.write_text(json.dumps(run.manifest()))
            self.assertEqual(validate_candidate_manifest(path), (0, []))

    def test_network_error_run_keeps_the_error_and_fabricates_nothing(self):
        run = make_adapter().collect("网络错误")
        self.assertEqual(run.search.status, SearchStatus.ERROR)
        self.assertEqual(run.candidates, ())
        self.assertEqual(len(run.failures), 1)
        self.assertEqual(run.failures[0].stage, "search")
        self.assertEqual(run.audit()["search"]["error"]["code"], "timeout")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidates.json"
            path.write_text(json.dumps(run.manifest()))
            self.assertEqual(validate_candidate_manifest(path), (0, []))

    def test_missing_fields_are_recorded_not_filled(self):
        run = make_adapter().collect("缺失字段")
        self.assertEqual(run.candidates, ())
        self.assertTrue(any(
            failure.stage == "normalize" and failure.field == "title"
            for failure in run.failures
        ))
        self.assertTrue(any(failure.stage == "fetch" for failure in run.failures))

    def test_run_audit_is_separate_and_complete(self):
        run = make_adapter().collect("合成合同审查")
        audit = run.audit()
        self.assertTrue(audit["run_id"].startswith("disc-"))
        self.assertEqual(audit["query"], "合成合同审查")
        self.assertEqual(audit["candidate_status"], {"candidate": 1, "needs-evidence": 1})
        self.assertEqual(audit["regulatory_currency"], {"not-checked": 2})
        self.assertEqual(audit["content_withheld"], 1)
        self.assertEqual(audit["duplicates"][0]["reason"], "same canonical source entry")
        self.assertTrue(audit["notes"])

    def test_candidate_and_formal_contracts_remain_separate(self):
        run = make_adapter().collect("合成合同审查")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "candidates.json"
            path.write_text(json.dumps(run.manifest()))
            self.assertEqual(validate_candidate_manifest(path), (2, []))
            count, errors = validate_formal_metadata([path])
        self.assertEqual(count, 1)
        self.assertTrue(errors)
        self.assertTrue(any("/id" in error for error in errors))

    def test_pipeline_does_not_open_a_socket(self):
        with patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            run = make_adapter().collect("合成合同审查")
        self.assertEqual(len(run.candidates), 2)


class CLITests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(CLI), *(str(arg) for arg in args)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_success_writes_valid_manifest_and_audit(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "candidates.json"
            audit = Path(folder) / "audit.json"
            result = self.run_cli(
                "--query", "合成合同审查",
                "--output", output,
                "--audit", audit,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(validate_candidate_manifest(output), (2, []))
            record = json.loads(audit.read_text(encoding="utf-8"))
            self.assertEqual(record["search"]["status"], "ok")
            self.assertEqual(record["content_withheld"], 1)
            self.assertIn("search=ok", result.stderr)

    def test_empty_result_exits_zero_and_reports_zero(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "candidates.json"
            result = self.run_cli("--query", "空结果", "--output", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(validate_candidate_manifest(output), (0, []))
            self.assertIn("candidates=0", result.stderr)

    def test_network_error_exits_one(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "candidates.json"
            audit = Path(folder) / "audit.json"
            result = self.run_cli(
                "--query", "网络错误",
                "--output", output,
                "--audit", audit,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(validate_candidate_manifest(output), (0, []))
            self.assertEqual(
                json.loads(audit.read_text(encoding="utf-8"))["search"]["error"]["code"],
                "timeout",
            )

    def test_refuses_to_write_anywhere_in_repository(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as folder:
            target = Path(folder) / "out.json"
            result = self.run_cli("--query", "空结果", "--output", target)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse(target.exists())

    def test_refuses_same_output_and_audit_path(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "same.json"
            result = self.run_cli(
                "--query", "空结果",
                "--output", path,
                "--audit", path,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse(path.exists())

    def test_refuses_to_overwrite_an_existing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "existing.json"
            path.write_text("KEEP", encoding="utf-8")
            result = self.run_cli("--query", "空结果", "--output", path)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(path.read_text(encoding="utf-8"), "KEEP")

    def test_no_output_when_audit_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "out.json"
            audit = ROOT / "data" / "discovery" / "audit-should-not-exist.json"
            result = self.run_cli(
                "--query", "空结果",
                "--output", output,
                "--audit", audit,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse(output.exists())
            self.assertFalse(audit.exists())

    def test_precheck_rejects_repository_file_and_symlink_alias(self):
        with tempfile.TemporaryDirectory() as folder:
            alias = Path(folder) / "alias.json"
            alias.symlink_to(ROOT / "README.md")
            for target in (ROOT / "README.md", alias):
                with self.subTest(target=target):
                    with self.assertRaises(ValueError):
                        offline_cli.precheck_outputs([("candidate manifest", target)])

    def test_refuses_to_write_into_candidate_or_skills_directories(self):
        for relative in ("data/discovery/offline-should-not-exist.json", "skills/offline-should-not-exist.json"):
            with self.subTest(relative=relative):
                target = ROOT / relative
                self.assertFalse(target.exists())
                result = self.run_cli("--query", "空结果", "--output", target)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("refusing to write", result.stderr)
                self.assertFalse(target.exists())

    def test_missing_fixture_and_bad_arguments_exit_two(self):
        result = self.run_cli(
            "--query", "合成合同审查",
            "--search-fixture", ROOT / "tests" / "fixtures" / "discovery" / "missing.json",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot load fixtures", result.stderr)
        self.assertEqual(self.run_cli().returncode, 2)


if __name__ == "__main__":
    unittest.main()
