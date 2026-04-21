#!/usr/bin/env python3
"""
COVERAGE_HOLE_ANALYZER
Consumes a simple "metric value" text report and highlights low-coverage points.
Also cross-references testplan traceability matrix (JSON).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

LINE_RE = re.compile(r"^\s*([A-Za-z0-9_./:-]+)\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)\s*%?\s*$")


def load_metrics(path: Path) -> dict[str, float]:
    metrics: dict[str, float] = {}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = LINE_RE.match(line)
        if m:
            metrics[m.group(1)] = float(m.group(2))
    return metrics


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("coverage_report", type=Path, help="text file: metric: xx")
    ap.add_argument("--threshold", type=float, default=90.0)
    ap.add_argument(
        "--trace",
        type=Path,
        default=Path("../testplan/traceability.json"),
        help="traceability matrix json",
    )
    args = ap.parse_args()

    if not args.coverage_report.exists():
        raise SystemExit(f"coverage report not found: {args.coverage_report}")

    metrics = load_metrics(args.coverage_report)
    if not metrics:
        raise SystemExit("no metrics parsed; expected lines like 'cp_arc: 78.5'")

    holes = [(k, v) for k, v in sorted(metrics.items()) if v < args.threshold]

    trace = {}
    if args.trace.exists():
        trace = json.loads(args.trace.read_text(encoding="utf-8"))

    print("=== COVERAGE_HOLE_ANALYZER ===")
    print(f"report: {args.coverage_report}")
    print(f"threshold: {args.threshold:.1f}%")
    print(f"metrics: {len(metrics)}")
    print(f"holes: {len(holes)}")

    if not holes:
        print("No coverage holes found.")
        return 0

    suggestions = trace.get("coverage_to_tests", {}) if isinstance(trace, dict) else {}

    for name, val in holes:
        print(f"- {name}: {val:.1f}%")
        if name in suggestions:
            mapped = ", ".join(suggestions[name])
            print(f"  suggested tests: {mapped}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
