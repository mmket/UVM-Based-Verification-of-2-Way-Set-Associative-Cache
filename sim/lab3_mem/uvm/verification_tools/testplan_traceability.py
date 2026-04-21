#!/usr/bin/env python3
"""
TESTPLAN_TRACEABILITY
Checks that mapped tests / assertions / coverage points exist.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--trace",
        type=Path,
        default=Path("../testplan/traceability.json"),
        help="traceability json",
    )
    ap.add_argument("--uvm_dir", type=Path, default=Path(".."))
    args = ap.parse_args()

    if not args.trace.exists():
        raise SystemExit(f"traceability file not found: {args.trace}")

    data = json.loads(args.trace.read_text(encoding="utf-8"))

    tests_text = text(args.uvm_dir / "cache_tests.svh")
    assert_text = text(args.uvm_dir / "cache_alt_ctrl_bind.sv") + "\n" + text(args.uvm_dir / "cache_sva_assertion_writer.sv")

    print("=== TESTPLAN_TRACEABILITY ===")

    missing = 0

    for feat in data.get("features", []):
        name = feat.get("name", "<unnamed>")
        test_refs = feat.get("tests", [])
        asrt_refs = feat.get("assertions", [])
        cov_refs = feat.get("coverage", [])

        print(f"Feature: {name}")

        for t in test_refs:
            ok = t in tests_text
            print(f"  test      {t:35s} {'OK' if ok else 'MISSING'}")
            missing += 0 if ok else 1

        for a in asrt_refs:
            ok = a in assert_text
            print(f"  assertion {a:35s} {'OK' if ok else 'MISSING'}")
            missing += 0 if ok else 1

        for c in cov_refs:
            ok = c in assert_text
            print(f"  coverage  {c:35s} {'OK' if ok else 'MISSING'}")
            missing += 0 if ok else 1

    print(f"\\nmissing_links: {missing}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
