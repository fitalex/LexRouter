#!/usr/bin/env python3
"""Run the Discovery adapter against local synthetic fixtures only.

This command never contacts a search or fetch endpoint and never schedules a
run.  It refuses to write anywhere inside this repository, refuses to overwrite
an existing file, and writes the candidate manifest plus optional audit as one
all-or-nothing pair.  Historical candidate manifests therefore cannot be
overwritten by an offline prototype run.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile


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


def precheck_outputs(outputs):
    """Validate every output path before any write.

    ``outputs`` is an iterable of ``(label, path)``.  The check rejects a path
    inside the repository worktree (including symlink aliases), an existing
    path, a missing parent, and two labels resolving to the same path.
    """
    planned = []
    seen = {}
    for label, path in outputs:
        target = Path(path)
        try:
            resolved = target.resolve()
        except (OSError, RuntimeError) as exc:
            raise ValueError(f"cannot resolve {label} path {target}: {exc}") from exc
        if resolved in seen:
            raise ValueError(
                f"{label} and {seen[resolved]} resolve to the same path: {resolved}"
            )
        seen[resolved] = label
        if resolved == ROOT or ROOT in resolved.parents:
            raise ValueError(
                f"refusing to write {label} inside the repository worktree: {resolved}"
            )
        if os.path.lexists(target):
            raise ValueError(f"refusing to overwrite existing {label}: {target}")
        if not resolved.parent.is_dir():
            raise ValueError(f"{label} parent directory does not exist: {resolved.parent}")
        planned.append((label, target, resolved))
    return planned


def write_outputs(outputs):
    """Write ``(label, path, text)`` items with preflight and rollback.

    All paths are checked before the first byte is written.  Temporary files
    are linked into place without replacing an existing target; if any later
    write fails, targets created by this call are removed.
    """
    items = list(outputs)
    planned = precheck_outputs((label, path) for label, path, _ in items)
    temporary = []
    written = []
    try:
        for (_, target, resolved), (_, _, text) in zip(planned, items):
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{target.name}.",
                suffix=".tmp",
                dir=str(resolved.parent),
            )
            temporary.append((target, Path(temporary_name)))
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(text)
        for target, temporary_name in temporary:
            # A hard link fails rather than overwriting a target that appeared
            # after the preflight check; the temporary file stays in the same
            # directory, so both paths are on the same filesystem.
            os.link(temporary_name, target)
            temporary_name.unlink()
            written.append(target)
    except (OSError, ValueError):
        for _, temporary_name in temporary:
            try:
                temporary_name.unlink()
            except FileNotFoundError:
                pass
        for target in written:
            try:
                target.unlink()
            except FileNotFoundError:
                pass
        raise


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
    file_outputs = []
    if args.output:
        file_outputs.append(("candidate manifest", args.output, manifest))
    if args.audit:
        file_outputs.append(("run audit", args.audit, audit))

    try:
        write_outputs(file_outputs)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot write output: {exc}", file=sys.stderr)
        return 2

    for label, path, _ in file_outputs:
        print(f"wrote {label} to {Path(path).resolve()}", file=sys.stderr)
    if not args.output:
        print(manifest, end="")

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
