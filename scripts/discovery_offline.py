#!/usr/bin/env python3
"""Run the Discovery adapter against local synthetic fixtures only.

This command never contacts a search or fetch endpoint and never schedules a
run.  Output files are written only into a new private directory created by
this process, with fixed names ``candidates.json`` and ``audit.json``.  No
arbitrary output file path, existing file or repository path is accepted.
"""

import argparse
import json
import os
from pathlib import Path
import stat
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from discovery import DiscoveryAdapter  # noqa: E402


DEFAULT_SEARCH = ROOT / "tests" / "fixtures" / "discovery" / "search_responses.json"
DEFAULT_SOURCES = ROOT / "tests" / "fixtures" / "discovery" / "sources.json"
OUTPUT_MANIFEST = "candidates.json"
OUTPUT_AUDIT = "audit.json"


class OutputWriteError(Exception):
    """A failed output publication that may have left residual files."""

    def __init__(self, message, *, residual=(), cleanup_errors=()):
        super().__init__(message)
        self.residual = tuple(residual)
        self.cleanup_errors = tuple(cleanup_errors)


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def _within_repository(path):
    resolved = Path(path).resolve()
    return resolved == ROOT or ROOT in resolved.parents


def _fd_path(descriptor):
    """Resolve an open directory descriptor without reusing a mutable path."""
    try:
        return Path(os.readlink(f"/proc/self/fd/{descriptor}"))
    except OSError:
        pass
    try:
        import fcntl

        value = fcntl.fcntl(descriptor, fcntl.F_GETPATH, b"\0" * 1024)
        return Path(value.split(b"\0", 1)[0].decode("utf-8", "surrogateescape"))
    except (ImportError, OSError, AttributeError, ValueError):
        return None


def _resolve_output_parent(path):
    target = Path(path)
    if os.path.lexists(target):
        raise ValueError(f"output directory must not already exist: {target}")
    name = target.name
    if name in {"", ".", ".."}:
        raise ValueError(f"output directory needs a new leaf name: {target}")
    parent = target.parent
    try:
        parent = parent.resolve()
    except (OSError, RuntimeError) as exc:
        raise ValueError(f"cannot resolve output parent {parent}: {exc}") from exc
    if _within_repository(parent):
        raise ValueError(f"refusing to write inside the repository worktree: {parent}")
    if not parent.is_dir():
        raise ValueError(f"output parent directory does not exist: {parent}")
    return parent, name


def _create_private_dir(path):
    """Create a new 0700 directory relative to an opened parent descriptor."""
    parent, name = _resolve_output_parent(path)
    parent_fd = None
    dir_fd = None
    created_dir = False
    created_info = None
    try:
        parent_fd = os.open(parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        actual_parent = _fd_path(parent_fd)
        if actual_parent is None:
            raise ValueError("cannot verify the output parent directory identity")
        if _within_repository(actual_parent):
            raise ValueError(f"refusing to write inside the repository worktree: {actual_parent}")
        os.mkdir(name, 0o700, dir_fd=parent_fd)
        created_dir = True
        created_info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        dir_fd = os.open(
            name,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=parent_fd,
        )
        actual_dir = _fd_path(dir_fd)
        if actual_dir is None:
            raise ValueError("cannot verify the output directory identity")
        if _within_repository(actual_dir):
            raise ValueError(f"refusing to write inside the repository worktree: {actual_dir}")
        info = os.fstat(dir_fd)
        return parent_fd, dir_fd, name, actual_dir, (info.st_dev, info.st_ino)
    except Exception:
        if dir_fd is not None:
            os.close(dir_fd)
        if parent_fd is not None:
            if created_dir and created_info is not None:
                try:
                    current = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
                    if (current.st_dev, current.st_ino) == (
                        created_info.st_dev, created_info.st_ino
                    ):
                        os.rmdir(name, dir_fd=parent_fd)
                except OSError:
                    pass
            os.close(parent_fd)
        raise


def _write_file(dir_fd, name, text, created):
    descriptor = os.open(
        name,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
        dir_fd=dir_fd,
    )
    try:
        info = os.fstat(descriptor)
    except OSError:
        os.close(descriptor)
        raise
    # Keep the descriptor open until publication finishes.  The open inode
    # cannot be reused, so a later replacement necessarily has another inode.
    created.append((name, descriptor, info.st_dev, info.st_ino))
    remaining = memoryview(text.encode("utf-8"))
    while remaining:
        written = os.write(descriptor, remaining)
        if written <= 0:
            raise OSError("short write while publishing output")
        remaining = remaining[written:]


def _close_created(created):
    for _, descriptor, _, _ in created:
        try:
            os.close(descriptor)
        except OSError:
            pass


def _rollback_outputs(dir_fd, name, parent_fd, dir_identity, created):
    """Best-effort cleanup of objects this run created; never trust a pathname alone."""
    residual = []
    cleanup_errors = []
    for file_name, _descriptor, device, inode in reversed(created):
        try:
            info = os.stat(file_name, dir_fd=dir_fd, follow_symlinks=False)
        except FileNotFoundError:
            continue
        except OSError as exc:
            cleanup_errors.append(f"{file_name}: cannot inspect ({exc})")
            residual.append(file_name)
            continue
        if (info.st_dev, info.st_ino) != (device, inode) or not stat.S_ISREG(info.st_mode):
            cleanup_errors.append(f"{file_name}: replaced by another writer; preserved")
            residual.append(file_name)
            continue
        try:
            os.unlink(file_name, dir_fd=dir_fd)
        except FileNotFoundError:
            continue
        except OSError as exc:
            cleanup_errors.append(f"{file_name}: cannot remove ({exc})")
            residual.append(file_name)

    try:
        remaining = sorted(os.listdir(dir_fd))
    except OSError as exc:
        remaining = None
        cleanup_errors.append(f"cannot list output directory ({exc})")
    if remaining is not None:
        residual = sorted(set(residual) | set(remaining))
        if not remaining:
            try:
                info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            except OSError as exc:
                cleanup_errors.append(f"cannot inspect output directory ({exc})")
            else:
                if (info.st_dev, info.st_ino) == dir_identity and stat.S_ISDIR(info.st_mode):
                    try:
                        os.rmdir(name, dir_fd=parent_fd)
                    except OSError as exc:
                        cleanup_errors.append(f"cannot remove empty output directory ({exc})")
                else:
                    cleanup_errors.append("output directory was replaced; preserved")
    return residual, cleanup_errors


def write_output_dir(path, manifest, audit):
    """Publish both files into one new private directory, or fail nonzero."""
    parent_fd = None
    dir_fd = None
    created = []
    try:
        parent_fd, dir_fd, name, actual_dir, dir_identity = _create_private_dir(path)
        try:
            _write_file(dir_fd, OUTPUT_MANIFEST, manifest, created)
            _write_file(dir_fd, OUTPUT_AUDIT, audit, created)
        except Exception as exc:
            residual, cleanup_errors = _rollback_outputs(
                dir_fd, name, parent_fd, dir_identity, created
            )
            detail = f"{actual_dir}: {exc}"
            if residual:
                detail += f"; residual: {', '.join(residual)}"
            if cleanup_errors:
                detail += f"; cleanup: {'; '.join(cleanup_errors)}"
            raise OutputWriteError(
                detail,
                residual=residual,
                cleanup_errors=cleanup_errors,
            ) from exc
        return actual_dir
    finally:
        _close_created(created)
        if dir_fd is not None:
            os.close(dir_fd)
        if parent_fd is not None:
            os.close(parent_fd)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--query", required=True, help="fixture query key; no external request")
    parser.add_argument("--search-fixture", default=str(DEFAULT_SEARCH), help="synthetic search response JSON")
    parser.add_argument("--source-fixture", default=str(DEFAULT_SOURCES), help="synthetic pinned-source JSON")
    parser.add_argument("--limit", type=positive_int, default=20, help="maximum hits to process")
    parser.add_argument(
        "--output-dir",
        help="new private directory for candidates.json and audit.json (default: manifest on stdout)",
    )
    args = parser.parse_args(argv)

    try:
        adapter = DiscoveryAdapter.from_fixtures(args.search_fixture, args.source_fixture)
        run = adapter.collect(args.query, limit=args.limit)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: cannot load fixtures or run the adapter: {exc}", file=sys.stderr)
        return 2

    manifest = json.dumps(run.manifest(), ensure_ascii=False, indent=2) + "\n"
    audit = json.dumps(run.audit(), ensure_ascii=False, indent=2) + "\n"

    if args.output_dir:
        try:
            published = write_output_dir(args.output_dir, manifest, audit)
        except (OSError, ValueError, OutputWriteError) as exc:
            print(f"FAIL: cannot publish output directory: {exc}", file=sys.stderr)
            return 2
        print(f"wrote {OUTPUT_MANIFEST} and {OUTPUT_AUDIT} to {published}", file=sys.stderr)
    else:
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
