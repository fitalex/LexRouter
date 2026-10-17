#!/usr/bin/env python3
"""Validate candidate batches together offline; semantic deduplication is manual."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from validate_candidates import reject_constant, unique_object, validate


SHA = re.compile(r"^[0-9a-f]{40}$")


def source_identity(url):
    """Ignore GitHub revision, URL presentation and host/repository casing.

    File paths remain case sensitive. Forks, mirrors and copied prompts require
    source research and manual comparison; this key cannot identify them.
    """
    parsed = urlsplit(url)
    host = (parsed.hostname or "").lower()
    parts = unquote(parsed.path).strip("/").split("/")
    if host in {"github.com", "www.github.com"} and len(parts) >= 5:
        if parts[2] in {"blob", "raw"}:
            return ("github", parts[0].lower(), parts[1].lower(), "/".join(parts[4:]))
    if host == "raw.githubusercontent.com" and len(parts) >= 4:
        return ("github", parts[0].lower(), parts[1].lower(), "/".join(parts[3:]))
    return (host, parsed.path, parsed.query)


def validate_batches(paths):
    """Return records and diagnostics; invalid input never contributes statistics."""
    records, errors, seen_paths, seen_ids, seen_sources = [], [], set(), {}, {}
    for value in paths:
        path = Path(value)
        resolved = path.resolve()
        if resolved in seen_paths:
            errors.append(f"{path}: /: repeated input manifest")
            continue
        seen_paths.add(resolved)
        _, diagnostics = validate(path)
        if diagnostics:
            errors.extend(diagnostics)
            continue
        data = json.loads(path.read_text(encoding="utf-8"),
                          object_pairs_hook=unique_object, parse_constant=reject_constant)
        for index, record in enumerate(data["candidates"]):
            location = f"{path}: /candidates/{index}"
            candidate_id = record["candidate_id"]
            if candidate_id in seen_ids:
                errors.append(f"{location}/candidate_id: duplicate candidate ID {candidate_id!r}; "
                              f"first seen at {seen_ids[candidate_id]}")
            else:
                seen_ids[candidate_id] = location
            identity = source_identity(record["source_url"])
            if identity in seen_sources:
                errors.append(f"{location}/source_url: duplicate source entry across revisions/runtimes; "
                              f"first seen at {seen_sources[identity]}; manual capability review required")
            else:
                seen_sources[identity] = location
            revision = record["source_verification"]["revision"]
            if not SHA.fullmatch(revision):
                errors.append(f"{location}/source_verification/revision: batch review requires full commit SHA")
            parsed = urlsplit(record["source_url"])
            parts = unquote(parsed.path).strip("/").split("/")
            host = (parsed.hostname or "").lower()
            pinned = False
            if host in {"github.com", "www.github.com"} and len(parts) >= 5:
                pinned = parts[2] in {"blob", "raw"} and parts[3] == revision
            elif host == "raw.githubusercontent.com" and len(parts) >= 4:
                pinned = parts[2] == revision
            if not pinned:
                errors.append(f"{location}/source_url: expected original GitHub file pinned to revision")
            if record["source_url"] not in record["source_verification"]["evidence_urls"]:
                errors.append(f"{location}/source_verification/evidence_urls: missing entry evidence")
            records.append(record)
    return records, errors


def summary(records):
    return {
        "records": len(records),
        "candidate_status": dict(sorted(Counter(r["candidate_status"] for r in records).items())),
        "authorization": dict(sorted(Counter(r["authorization"]["status"] for r in records).items())),
        "business_categories": dict(sorted(Counter(c for r in records for c in r["business_categories"]).items())),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="explicit candidate JSON manifests; no network access")
    args = parser.parse_args(argv)
    try:
        records, errors = validate_batches(args.paths)
    except (OSError, UnicodeError, ValueError) as exc:
        records, errors = [], [f"/: validation setup/read error: {exc}"]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"FAIL: {len(errors)} batch error(s); no deduplicated count certified.", file=sys.stderr)
        return 1
    print(f"PASS: {len(records)} records across {len(args.paths)} manifest(s); unique IDs/source entries.")
    print(json.dumps(summary(records), ensure_ascii=False, sort_keys=True))
    print("Offline structure/source checks only; forks, mirrors and semantic capability duplicates "
          "require manual review. No legal/license approval or formal admission.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
