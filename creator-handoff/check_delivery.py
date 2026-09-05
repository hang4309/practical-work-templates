#!/usr/bin/env python3
"""Check listed files and a deliberately small UTF-8 SRT handoff contract.

Python 3.10+, standard library only. Reads files; writes only JSON to stdout.
Streaming SHA-256 pattern adapted from asset 1220; see SOURCE_NOTICES.md.
This is not a media decoder, subtitle editor, or rights/approval decision.
"""
import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path, PurePosixPath

STAMP = r"(\d{2}):([0-5]\d):([0-5]\d),(\d{3})"
CUE_TIME = re.compile(STAMP + r" --> " + STAMP)
MAX_MANIFEST_BYTES = 1024 * 1024
MAX_SRT_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 2 * 1024 * 1024 * 1024


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def local_file(root, value):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError("expected a relative path with forward slashes")
    rel = PurePosixPath(value)
    if rel.is_absolute() or ".." in rel.parts or str(rel) != value:
        raise ValueError("path must stay inside the delivery directory")
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError("resolved path leaves the delivery directory")
    if not path.is_file():
        raise ValueError("listed file is missing or is not a regular file")
    return path


def milliseconds(parts):
    h, m, s, ms = map(int, parts)
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def srt_issues(path, duration_ms):
    if path.stat().st_size > MAX_SRT_BYTES:
        return ["SRT exceeds the 2 MiB limit"], 0
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeError:
        return ["SRT must be UTF-8"], 0
    blocks = re.split(r"\n\s*\n", text.strip().replace("\r\n", "\n")) if text.strip() else []
    issues, previous_end = [], 0
    if not blocks:
        issues.append("SRT contains no cues")
    for number, block in enumerate(blocks, 1):
        lines = block.splitlines()
        match = CUE_TIME.fullmatch(lines[1]) if len(lines) >= 3 else None
        if not lines or lines[0] != str(number) or not match or not any(x.strip() for x in lines[2:]):
            issues.append(f"cue {number}: expected sequential number, strict time line, and nonempty text")
            continue
        start, end = milliseconds(match.groups()[:4]), milliseconds(match.groups()[4:])
        if end <= start:
            issues.append(f"cue {number}: end must be after start")
        if start < previous_end:
            issues.append(f"cue {number}: overlap or backward order")
        if end > duration_ms:
            issues.append(f"cue {number}: extends beyond declared picture duration")
        previous_end = end
    return issues, len(blocks)


def check(manifest_path):
    root = manifest_path.resolve().parent
    if manifest_path.stat().st_size > MAX_MANIFEST_BYTES:
        raise ValueError("manifest exceeds 1 MiB")
    data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("expected schema_version 1 object")
    assets, picture = data.get("assets"), data.get("picture")
    if not isinstance(assets, list) or not 1 <= len(assets) <= 200:
        raise ValueError("assets must contain between 1 and 200 entries")
    if not isinstance(picture, dict) or not isinstance(picture.get("version"), str) or not picture["version"].strip():
        raise ValueError("picture must declare a nonempty version")
    duration = picture.get("duration_seconds")
    if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(duration) or not 0 < duration <= 86400:
        raise ValueError("picture duration must be positive and at most 86400 seconds")
    findings, checked, seen, total_bytes = [], [], set(), 0
    def issue(path, code, detail):
        findings.append({"path": path, "code": code, "detail": detail})
    picture_found = False
    for item in assets:
        if not isinstance(item, dict):
            issue("(entry)", "BAD_ENTRY", "asset must be an object")
            continue
        rel = item.get("path")
        if not isinstance(rel, str):
            issue("(entry)", "BAD_PATH", "path must be text")
            continue
        if rel in seen:
            issue(rel, "DUPLICATE_PATH", "list each path once")
            continue
        seen.add(rel)
        try:
            path = local_file(root, rel)
        except (ValueError, OSError) as exc:
            issue(rel, "FILE_UNAVAILABLE", str(exc))
            continue
        size = path.stat().st_size
        total_bytes += size
        if total_bytes > MAX_TOTAL_BYTES:
            raise ValueError("listed file bytes exceed the 2 GiB work limit")
        expected = item.get("sha256")
        if not isinstance(expected, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", expected):
            issue(rel, "MISSING_HASH", "every listed file needs a 64-hex SHA-256")
            continue
        digest = sha256(path)
        if digest.lower() != expected.lower():
            issue(rel, "HASH_MISMATCH", "bytes differ from the declared delivery")
        if item.get("role") == "picture" and rel == picture.get("path"):
            picture_found = True
        record = {"path": rel, "bytes": size, "sha256": digest}
        if item.get("role") == "subtitle":
            if path.suffix.lower() != ".srt":
                issue(rel, "UNSUPPORTED_SUBTITLE", "this checker only supports strict UTF-8 SRT")
            else:
                problems, count = srt_issues(path, round(duration * 1000))
                record["cue_count"] = count
                for problem in problems:
                    issue(rel, "SRT_TIMING_OR_FORMAT", problem)
            if item.get("picture_version") != picture["version"]:
                issue(rel, "PICTURE_VERSION_MISMATCH", "subtitle is bound to another picture version")
            if not isinstance(item.get("language"), str) or not item["language"].strip():
                issue(rel, "MISSING_LANGUAGE", "declare the subtitle language explicitly")
        checked.append(record)
    if not picture_found:
        issue(str(picture.get("path")), "MISSING_PICTURE", "picture.path must name an existing listed picture asset with a hash")
    # A structurally consistent folder is not an approval to publish it.
    return {
        "schema_version": 1,
        "file_check": "consistent" if not findings else "needs_attention",
        "project": data.get("project"),
        "checked_files": checked,
        "findings": findings,
        "manual_review": data.get("manual_review", {}),
        "limits": ["Checks listed paths, hashes, SRT timing and declared picture version only.",
                   "Unlisted files are not inventoried; directory contents are not an allowlist for publication.",
                   "Does not decode media or prove duration, translation, audio sync, rights, or client approval.",
                   "Use on a stable local folder; files must not change during the check."]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        result = check(args.manifest)
    except (ValueError, OSError, TypeError) as exc:
        print(json.dumps({"file_check": "invalid_input", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["file_check"] == "consistent" else 1


if __name__ == "__main__":
    sys.exit(main())
