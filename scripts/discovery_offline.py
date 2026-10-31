#!/usr/bin/env python3
"""Run the Discovery adapter against local synthetic fixtures only.

This command never contacts a search or fetch endpoint and never schedules a
run.  It refuses to write candidate or audit output into ``data/discovery/`` or
``skills/`` so the historical candidate manifests cannot be overwritten by an
offline prototype run.
"""

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from discovery import DiscoveryAdapter  # noqa: E402


DEFAULT_SEARCH = ROOT / "tests" / "fixtures" / "discovery" / "search_responses.json"
DEFAULT_SOURCES = ROOT / "tests" / "fixtures" / "discovery" / "sources.json"


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def forbidden_directory(path):
    target = Path(path).resolve()
    for directory in (ROOT / "data" / "discovery", ROOT / "skills"):
        if target == directory or directory in target.parents:
            return directory
    return None


def write_text(path, text):
    target = Path(path)
    forbidden = forbidden_directory(target)
    if forbidden is not None:
        raise ValueError(
            f"refusing to write {target} under {forbidden}; "
            "pass a temporary path and review the output before any manual promotion"
        )
    target.write_text(text, encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="fixture query key; no external request")
    parser.add_argument("--search-fixture", default=str(DEFAULT_SEARCH), help="synthetic search response JSON")
    parser.add_argument("--source-fixture", default=str(DEFAULT_SOURCES), help="synthetic pinned-source JSON")
    parser.add_argument("--limit", type=positive_int, default=20, help="maximum hits to process")
    parser.add_argument("--output", help="candidate manifest path (default: stdout)")
    parser.add_argument("--audit", help="optional run-audit JSON path")
    args = parser.parse_args(argv)

    try:
        adapter = DiscoveryAdapter.from_fixtures(args.search_fixture, args.source_fixture)
        run = adapter.collect(args.query, limit=args.limit)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: cannot load fixtures or run the adapter: {exc}", file=sys.stderr)
        return 2

    manifest = json.dumps(run.manifest(), ensure_ascii=False, indent=2) + "\n"
    audit = json.dumps(run.audit(), ensure_ascii=False, indent=2) + "\n"
    try:
        if args.output:
            write_text(args.output, manifest)
            print(f"wrote candidate manifest to {Path(args.output).resolve()}", file=sys.stderr)
        else:
            print(manifest, end="")
        if args.audit:
            write_text(args.audit, audit)
            print(f"wrote run audit to {Path(args.audit).resolve()}", file=sys.stderr)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot write output: {exc}", file=sys.stderr)
        return 2

    record = run.audit()
    print(
        "search={status} hits={hits} candidates={candidates} duplicates={duplicates} "
        "failures={failures} content_withheld={content_withheld}".format(
            status=record["search"]["status"],
            hits=record["search"]["hits"],
            candidates=record["candidates"],
            duplicates=len(record["duplicates"]),
            failures=len(record["failures"]),
            content_withheld=record["content_withheld"],
        ),
        file=sys.stderr,
    )
    print("Offline synthetic fixtures only; no network, API key, scheduler or legal review.", file=sys.stderr)
    return 1 if run.failures else 0


if __name__ == "__main__":
    sys.exit(main())
