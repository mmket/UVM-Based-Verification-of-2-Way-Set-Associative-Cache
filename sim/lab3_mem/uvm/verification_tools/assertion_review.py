#!/usr/bin/env python3
"""
ASSERTION_REVIEW
Parse simulation logs and summarize assertion/uvm failures.
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

FAIL_PATTERNS = [
    re.compile(r"\bUVM_(FATAL|ERROR)\b"),
    re.compile(r"\bAssertion\b.*\bfailed\b", re.IGNORECASE),
    re.compile(r"\$error", re.IGNORECASE),
    re.compile(r"\[SVA_ASSERTION_WRITER\]", re.IGNORECASE),
]

WARN_PATTERNS = [
    re.compile(r"\bUVM_WARNING\b"),
    re.compile(r"\$warning", re.IGNORECASE),
]


def classify(line: str) -> str | None:
    if any(p.search(line) for p in FAIL_PATTERNS):
        return "fail"
    if any(p.search(line) for p in WARN_PATTERNS):
        return "warn"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("log", type=Path, help="simulator/UVM log file")
    ap.add_argument("--top", type=int, default=20, help="top lines to print")
    args = ap.parse_args()

    if not args.log.exists():
        raise SystemExit(f"log not found: {args.log}")

    counter = Counter()
    fail_lines: list[str] = []
    warn_lines: list[str] = []

    for raw in args.log.read_text(encoding="utf-8", errors="ignore").splitlines():
        kind = classify(raw)
        if not kind:
            continue
        counter[kind] += 1
        if kind == "fail":
            fail_lines.append(raw.strip())
        else:
            warn_lines.append(raw.strip())

    print("=== ASSERTION_REVIEW ===")
    print(f"log: {args.log}")
    print(f"fail_count: {counter['fail']}")
    print(f"warn_count: {counter['warn']}")

    if fail_lines:
        print("\\nTop failure lines:")
        for line in fail_lines[: args.top]:
            print(f"  - {line}")

    if warn_lines:
        print("\\nTop warning lines:")
        for line in warn_lines[: min(10, args.top)]:
            print(f"  - {line}")

    return 1 if counter["fail"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
