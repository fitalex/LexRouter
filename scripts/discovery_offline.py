#!/usr/bin/env python3
"""Run the Discovery adapter against local synthetic fixtures only.

This command never contacts a search or fetch endpoint and never schedules a
run.  Output is written only into a new private directory outside the repository,
with fixed ``candidates.json``, ``audit.json`` and ``complete.json`` names.

Security precondition: ``--output-dir`` must be under a trusted parent controlled
by the caller, with no untrusted same-UID process renaming entries in that parent
during the run.  The 0700 mode and descriptor identity checks detect many
replacement races after the directory is opened, but they do **not** defend
against a malicious same-UID writer that can control the parent directory before
the first directory identity is captured.  That case is UNSUPPORTED.

``complete.json`` is a byte-integrity marker, not proof that the run succeeded.
A consumer must bind the marker to a trustworthy exit status of that exact
invocation and also inspect ``audit.json``.  Failed publications never delete
already-written files; they exit nonzero and report residual paths.
"""

import argparse
import hashlib
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
OUTPUT_COMPLETE = "complete.json"


class OutputWriteError(Exception):
    """A failed output publication with any residual files and cleanup errors."""

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


def _check_directory_descriptor(descriptor, identity, expected_path=None):
    info = os.fstat(descriptor)
    if not stat.S_ISDIR(info.st_mode):
        raise OSError("output path is no longer a directory")
    if (info.st_dev, info.st_ino) != identity:
        raise OSError("output directory identity changed")
    if stat.S_IMODE(info.st_mode) != 0o700:
        raise OSError("output directory is not private (expected mode 0700)")
    if info.st_uid != os.geteuid():
        raise OSError("output directory owner changed")
    actual = _fd_path(descriptor)
    if actual is None:
        raise OSError("cannot verify the output directory identity")
    if expected_path is not None and actual != expected_path:
        raise OSError(f"output directory path changed: {actual}")
    if _within_repository(actual):
        raise OSError(f"output directory moved inside the repository: {actual}")


def _assert_directory_safe(descriptor, identity, expected_path):
    _check_directory_descriptor(descriptor, identity, expected_path)


def _retained_dir_state(parent_fd, name, identity):
    """Inspect a failed run directory; never delete it or its contents."""
    try:
        info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return [name], [f"{name}: output directory disappeared; location unknown"]
    except OSError as exc:
        return [name], [f"{name}: cannot inspect ({exc})"]
    if (info.st_dev, info.st_ino) != identity or not stat.S_ISDIR(info.st_mode):
        return [name], [f"{name}: replaced by another writer; preserved"]
    try:
        child_fd = os.open(
            name,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=parent_fd,
        )
        try:
            names = os.listdir(child_fd)
        finally:
            os.close(child_fd)
    except OSError as exc:
        return [name], [f"{name}: cannot list ({exc})"]
    if names:
        return sorted(names), []
    return [name], [f"{name}: empty output directory retained; automatic rmdir disabled"]


def _create_private_dir(path):
    """Create a new 0700 directory and bind every check to its opened fd.

    Trust boundary: the parent directory is controlled by the caller and no
    untrusted same-UID process renames entries there during the run.  A swap
    between mkdir and the first identity capture is UNSUPPORTED and is not
    claimed to be detected; checks after capture fail closed.
    """
    parent, name = _resolve_output_parent(path)
    parent_fd = None
    dir_fd = None
    created = False
    created_info = None
    try:
        parent_fd = os.open(parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        actual_parent = _fd_path(parent_fd)
        if actual_parent is None:
            raise OSError("cannot verify the output parent directory identity")
        if _within_repository(actual_parent):
            raise OSError(f"refusing to write inside the repository worktree: {actual_parent}")

        os.mkdir(name, 0o700, dir_fd=parent_fd)
        created = True
        created_info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        dir_fd = os.open(
            name,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=parent_fd,
        )
        info = os.fstat(dir_fd)
        if (info.st_dev, info.st_ino) != (
            created_info.st_dev, created_info.st_ino
        ):
            raise OSError("output directory was replaced between create and open")
        identity = (info.st_dev, info.st_ino)
        actual_dir = _fd_path(dir_fd)
        assert actual_dir is not None
        _check_directory_descriptor(dir_fd, identity, actual_dir)
        return parent_fd, dir_fd, name, actual_dir, identity
    except Exception as exc:
        residual = []
        cleanup_errors = []
        if dir_fd is not None:
            os.close(dir_fd)
            dir_fd = None
        if parent_fd is not None and created and created_info is not None:
            residual, cleanup_errors = _retained_dir_state(
                parent_fd, name, (created_info.st_dev, created_info.st_ino)
            )
        elif parent_fd is not None and created:
            residual = [name]
            cleanup_errors = [f"{name}: cannot inspect the created directory"]
        if parent_fd is not None:
            os.close(parent_fd)
            parent_fd = None
        if isinstance(exc, OutputWriteError):
            raise
        detail = f"{path}: {exc}"
        if residual:
            detail += f"; residual: {', '.join(residual)}"
        if cleanup_errors:
            detail += f"; cleanup: {'; '.join(cleanup_errors)}"
        raise OutputWriteError(
            detail,
            residual=residual,
            cleanup_errors=cleanup_errors,
        ) from exc


def _write_file(dir_fd, name, text, identity, expected_path):
    """Create one fixed file and return its content/inode identity."""
    _assert_directory_safe(dir_fd, identity, expected_path)
    descriptor = os.open(
        name,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
        dir_fd=dir_fd,
    )
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600:
            raise OSError(f"{name}: unexpected file mode")
        if info.st_uid != os.geteuid():
            raise OSError(f"{name}: unexpected file owner")
        payload = text.encode("utf-8")
        remaining = memoryview(payload)
        while remaining:
            written = os.write(descriptor, remaining)
            if written <= 0:
                raise OSError(f"{name}: short write")
            remaining = remaining[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    _assert_directory_safe(dir_fd, identity, expected_path)
    return hashlib.sha256(payload).hexdigest(), len(payload), info.st_dev, info.st_ino


def _read_file(dir_fd, name, identity, expected_path):
    _assert_directory_safe(dir_fd, identity, expected_path)
    descriptor = os.open(
        name,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
        dir_fd=dir_fd,
    )
    digest = hashlib.sha256()
    size = 0
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600:
            raise OSError(f"{name}: unexpected file mode")
        if info.st_uid != os.geteuid():
            raise OSError(f"{name}: unexpected file owner")
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
    finally:
        os.close(descriptor)
    _assert_directory_safe(dir_fd, identity, expected_path)
    return digest.hexdigest(), size


def _verify_file(dir_fd, name, expected, identity, expected_path):
    expected_hash, expected_size, expected_dev, expected_ino = expected
    info = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    if (
        not stat.S_ISREG(info.st_mode)
        or stat.S_IMODE(info.st_mode) != 0o600
        or info.st_uid != os.geteuid()
    ):
        raise OSError(f"{name}: no longer the published private file")
    if (info.st_dev, info.st_ino) != (expected_dev, expected_ino):
        raise OSError(f"{name}: replaced by another writer")
    digest, size = _read_file(dir_fd, name, identity, expected_path)
    if digest != expected_hash or size != expected_size:
        raise OSError(f"{name}: content changed after publication")


def _residual_names(dir_fd):
    try:
        return sorted(os.listdir(dir_fd))
    except OSError:
        return []


def write_output_dir(path, manifest, audit, run_status="unknown"):
    """Publish a byte-complete three-file run, or fail without deleting files."""
    parent_fd = None
    dir_fd = None
    try:
        parent_fd, dir_fd, name, actual_dir, identity = _create_private_dir(path)
        try:
            manifest_info = _write_file(
                dir_fd, OUTPUT_MANIFEST, manifest, identity, actual_dir
            )
            audit_info = _write_file(
                dir_fd, OUTPUT_AUDIT, audit, identity, actual_dir
            )
            _verify_file(
                dir_fd, OUTPUT_MANIFEST, manifest_info, identity, actual_dir
            )
            _verify_file(
                dir_fd, OUTPUT_AUDIT, audit_info, identity, actual_dir
            )

            complete = json.dumps({
                "format_version": 1,
                "status": "bytes-complete",
                "run_status": run_status,
                "candidates_sha256": manifest_info[0],
                "candidates_bytes": manifest_info[1],
                "audit_sha256": audit_info[0],
                "audit_bytes": audit_info[1],
            }, ensure_ascii=False, sort_keys=True) + "\n"
            complete_info = _write_file(
                dir_fd, OUTPUT_COMPLETE, complete, identity, actual_dir
            )

            # Re-check after the marker: a replacement before this point must
            # never be reported as a successful publication.
            _verify_file(
                dir_fd, OUTPUT_MANIFEST, manifest_info, identity, actual_dir
            )
            _verify_file(
                dir_fd, OUTPUT_AUDIT, audit_info, identity, actual_dir
            )
            _verify_file(
                dir_fd, OUTPUT_COMPLETE, complete_info, identity, actual_dir
            )
            _assert_directory_safe(dir_fd, identity, actual_dir)
        except Exception as exc:
            residual = _residual_names(dir_fd)
            cleanup_errors = []
            if not residual:
                residual, cleanup_errors = _retained_dir_state(
                    parent_fd, name, identity
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
        help="new private directory for candidates.json, audit.json and complete.json (default: manifest on stdout)",
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
        run_status = "ok" if not run.failures else "failed"
        try:
            published = write_output_dir(
                args.output_dir, manifest, audit, run_status=run_status
            )
        except (OSError, ValueError, OutputWriteError) as exc:
            print(f"FAIL: cannot publish output directory: {exc}", file=sys.stderr)
            return 2
        print(
            f"published {OUTPUT_MANIFEST}, {OUTPUT_AUDIT} and {OUTPUT_COMPLETE} "
            f"to {published} (run_status={run_status}, byte marker only)",
            file=sys.stderr,
        )
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
