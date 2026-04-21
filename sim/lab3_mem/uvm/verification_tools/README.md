# Verification Tools for lab3_mem

This directory implements the requested workflow capabilities:

- `SVA_ASSERTION_WRITER` -> `../cache_sva_assertion_writer.sv`
- `ASSERTION_REVIEW` -> `assertion_review.py`
- `COVERAGE_HOLE_ANALYZER` -> `coverage_hole_analyzer.py`
- `TESTPLAN_TRACEABILITY` -> `testplan_traceability.py` + `../testplan/traceability.json`

## Typical usage

```powershell
# 1) Run simulation (from uvm)
vsim -c -sv_seed 1 +UVM_TESTNAME=test_cache_random work.tb_top | Tee-Object sim.log

# 2) Assertion review
py -3 verification_tools/assertion_review.py sim.log

# 3) Coverage hole analysis (provide text report with "metric: value")
py -3 verification_tools/coverage_hole_analyzer.py coverage_summary.txt --threshold 90

# 4) Traceability consistency check
py -3 verification_tools/testplan_traceability.py
```

## Coverage report input format for analyzer

`coverage_hole_analyzer.py` parses simple lines like:

```text
cp_state: 100
cp_arc: 78.5
refill_upd_to_rdda: 92
```

This keeps it simulator-agnostic (you can export from Questa/VCS reports into a plain text summary).
