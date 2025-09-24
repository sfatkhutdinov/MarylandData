#!/usr/bin/env python3
"""
Provenance Audit for MarylandData (Hanover ZCTA 21076)

What this does:
- Verifies that persisted analysis outputs are traceable to raw sources with provenance
- Cross-checks a few metrics are consistent with raw inputs
- Scans for misplaced/duplicated raw files and reports suggested cleanups
- Produces a human-readable Markdown report under data/provenance_audit_report.md

This script performs only read operations; it will NOT move or modify files.
"""

from __future__ import annotations

import json
import os
import sys
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _read_json(path: str) -> Optional[Any]:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return None


def _file_hash(path: str, algo: str = 'sha256') -> Optional[str]:
    try:
        h = hashlib.new(algo)
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def _fmt_bool(b: bool) -> str:
    return 'PASS' if b else 'FAIL'


def _rel(path: str) -> str:
    try:
        return os.path.relpath(path, ROOT)
    except Exception:
        return path


def audit_hanover_real_data(report_lines: List[str]) -> Tuple[bool, List[str]]:
    ok = True
    notes: List[str] = []
    path = os.path.join(ROOT, 'data', 'hanover_real_data.json')
    exists = os.path.exists(path)
    report_lines.append(f"- data/hanover_real_data.json exists: {_fmt_bool(exists)}")
    if not exists:
        return False, ["Missing data/hanover_real_data.json"]

    doc = _read_json(path)
    if not isinstance(doc, dict):
        return False, ["Could not parse data/hanover_real_data.json as JSON object"]

    # Check ACS provenance
    acs = doc.get('raw_census_acs5')
    has_acs = isinstance(acs, dict) and isinstance(acs.get('provenance'), dict)
    report_lines.append(f"  • ACS block present with provenance: {_fmt_bool(has_acs)}")
    if not has_acs:
        ok = False
    else:
        prov = {}
        if isinstance(acs, dict):
            prov_candidate = acs['provenance'] if ('provenance' in acs and isinstance(acs['provenance'], dict)) else {}
            if isinstance(prov_candidate, dict):
                prov = prov_candidate
        raw_saved_to = prov.get('raw_saved_to')
        raw_exists = isinstance(raw_saved_to, str) and os.path.exists(os.path.join(ROOT, raw_saved_to) if not os.path.isabs(raw_saved_to) else raw_saved_to)
        report_lines.append(f"    – Referenced raw ACS file exists: {_fmt_bool(raw_exists)} ({_rel(raw_saved_to) if raw_saved_to else 'N/A'})")
        if not raw_exists:
            ok = False

    # Check Decennial provenance
    dec = doc.get('raw_census_decennial')
    has_dec = isinstance(dec, dict) and isinstance(dec.get('provenance'), dict)
    report_lines.append(f"  • Decennial block present with provenance: {_fmt_bool(has_dec)}")
    if not has_dec:
        ok = False
    else:
        prov = {}
        if isinstance(dec, dict):
            prov_candidate = dec['provenance'] if ('provenance' in dec and isinstance(dec['provenance'], dict)) else {}
            if isinstance(prov_candidate, dict):
                prov = prov_candidate
        raw_saved_to = prov.get('raw_saved_to')
        raw_exists = isinstance(raw_saved_to, str) and os.path.exists(os.path.join(ROOT, raw_saved_to) if not os.path.isabs(raw_saved_to) else raw_saved_to)
        report_lines.append(f"    – Referenced raw Decennial file exists: {_fmt_bool(raw_exists)} ({_rel(raw_saved_to) if raw_saved_to else 'N/A'})")
        if not raw_exists:
            ok = False

    # Cross-check a few metrics against raw ACS data
    metrics = doc.get('calculated_metrics', {}) or {}
    acs_data = (acs or {}).get('data', {}) or {}
    try:
        pop_raw = acs_data.get('B01003_001E', {}).get('value')
        pop_metric = metrics.get('population_2023')
        if pop_raw is not None and pop_metric is not None:
            pass_pop = int(pop_raw) == int(pop_metric)
            report_lines.append(f"  • population_2023 matches raw B01003_001E: {_fmt_bool(pass_pop)}")
            ok = ok and pass_pop
        else:
            notes.append("population_2023 or raw population missing; skip check")

        # price-to-income ratio check
        mhv = metrics.get('median_home_value')
        mhi = metrics.get('median_income')
        pti = metrics.get('price_to_income_ratio')
        if all(isinstance(x, (int, float)) for x in [mhv, mhi, pti]) and mhi:
            recomputed = mhv / mhi
            pass_pti = abs(recomputed - pti) < 1e-6
            report_lines.append(f"  • price_to_income_ratio consistent with median_home_value/median_income: {_fmt_bool(pass_pti)}")
            ok = ok and pass_pti
        else:
            notes.append("price_to_income_ratio check skipped (missing values)")

        # vacancy rate check if data present
        total_housing = acs_data.get('B25001_001E', {}).get('value')
        owner_occ = acs_data.get('B25003_002E', {}).get('value')
        renter_occ = acs_data.get('B25003_003E', {}).get('value')
        vacancy_metric = metrics.get('vacancy_rate')
        if all(isinstance(x, (int, float)) for x in [total_housing, owner_occ, renter_occ]) and isinstance(vacancy_metric, (int, float)):
            occupied_total = owner_occ + renter_occ
            recomputed_vac = ((total_housing - occupied_total) / total_housing) * 100
            pass_vac = abs(recomputed_vac - vacancy_metric) < 1e-6
            report_lines.append(f"  • vacancy_rate consistent with raw B25001/B25003: {_fmt_bool(pass_vac)}")
            ok = ok and pass_vac
        else:
            notes.append("vacancy_rate check skipped (missing values)")
    except Exception as e:
        report_lines.append(f"  • ERROR during metric cross-checks: {e}")
        ok = False

    return ok, notes


def audit_real_employment_income(report_lines: List[str]) -> Tuple[bool, List[str]]:
    ok = True
    notes: List[str] = []
    path = os.path.join(ROOT, 'data', 'real_employment_income.json')
    exists = os.path.exists(path)
    report_lines.append(f"- data/real_employment_income.json exists: {_fmt_bool(exists)}")
    if not exists:
        return False, ["Missing data/real_employment_income.json"]

    doc = _read_json(path)
    if not isinstance(doc, dict):
        return False, ["Could not parse data/real_employment_income.json as JSON object"]

    income = doc.get('income_distribution')
    employment = doc.get('employment_by_industry')
    affordability = doc.get('affordability_analysis')
    has_core = all(isinstance(x, dict) for x in [income, employment, affordability])
    report_lines.append(f"  • Contains income, employment, affordability blocks: {_fmt_bool(has_core)}")
    ok = ok and has_core

    # Affordability provenance
    prov = (affordability or {}).get('provenance', {})
    baseline_path = prov.get('baseline_metrics_path')
    baseline_exists = isinstance(baseline_path, str) and os.path.exists(os.path.join(ROOT, baseline_path) if not os.path.isabs(baseline_path) else baseline_path)
    report_lines.append(f"  • Affordability provenance baseline path exists: {_fmt_bool(baseline_exists)} ({_rel(baseline_path) if baseline_path else 'N/A'})")
    ok = ok and baseline_exists

    # Known gap: this ingestion does not currently cache raw API arrays
    notes.append("Raw API arrays for income/employment are not cached in data/raw; recommend enhancing ingestion to persist raw + provenance.")

    return ok, notes


def scan_raw_files(report_lines: List[str]) -> Tuple[List[str], List[Tuple[str, str]]]:
    """Scan for misplaced raw files and duplicates across data/raw and analysis/data/raw.

    Returns:
        misplaced: list of relative paths considered misplaced
        duplicates: list of (path_a, path_b) pairs with identical content
    """
    raw_dirs = [
        os.path.join(ROOT, 'data', 'raw'),
        os.path.join(ROOT, 'analysis', 'data', 'raw'),
    ]
    files: List[str] = []
    for d in raw_dirs:
        for root, _, fnames in os.walk(d):
            for fn in fnames:
                if fn.lower().endswith('.json') or fn.lower().endswith('.md'):
                    files.append(os.path.join(root, fn))

    report_lines.append(f"- Raw files discovered: {len(files)}")

    # Misplacement rule: prefer all raw census/API artifacts under data/raw/**
    misplaced: List[str] = []
    for f in files:
        rel = _rel(f)
        if rel.startswith('analysis/data/raw'):
            # Likely misplaced; analysis folder should not be the canonical raw store
            misplaced.append(rel)

    if misplaced:
        report_lines.append("  • Potentially misplaced raw files (prefer under data/raw/**):")
        for m in misplaced:
            report_lines.append(f"    – {m}")
    else:
        report_lines.append("  • No misplaced raw files detected")

    # Duplicate detection by content hash
    by_hash: Dict[str, List[str]] = {}
    for f in files:
        h = _file_hash(f)
        if h:
            by_hash.setdefault(h, []).append(f)

    duplicates: List[Tuple[str, str]] = []
    for paths in by_hash.values():
        if len(paths) > 1:
            # Record all unique pairs within this group
            for i in range(len(paths)):
                for j in range(i + 1, len(paths)):
                    duplicates.append((_rel(paths[i]), _rel(paths[j])))

    if duplicates:
        report_lines.append("  • Duplicate raw artifacts (identical content):")
        for a, b in duplicates:
            report_lines.append(f"    – {a} == {b}")
    else:
        report_lines.append("  • No duplicate raw artifacts detected")

    return misplaced, duplicates


def main() -> int:
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')
    lines: List[str] = []
    lines.append(f"# Provenance Audit Report\n")
    lines.append(f"Generated: {ts} UTC\n")

    lines.append("## Checks\n")
    overall_ok = True

    # Audit baseline data
    lines.append("### Baseline (data/hanover_real_data.json)\n")
    ok1, notes1 = audit_hanover_real_data(lines)
    overall_ok = overall_ok and ok1
    if notes1:
        lines.append("\nNotes:")
        for n in notes1:
            lines.append(f"- {n}")
    lines.append("")

    # Audit detailed employment/income
    lines.append("### Detailed (data/real_employment_income.json)\n")
    ok2, notes2 = audit_real_employment_income(lines)
    overall_ok = overall_ok and ok2
    if notes2:
        lines.append("\nNotes:")
        for n in notes2:
            lines.append(f"- {n}")
    lines.append("")

    # Scan raw file layout
    lines.append("### Raw file layout\n")
    misplaced, duplicates = scan_raw_files(lines)
    lines.append("")

    # Recommendations
    lines.append("## Recommendations\n")
    if misplaced:
        lines.append("- Move raw artifacts from analysis/data/raw/** into data/raw/** to make provenance centralized and clearer.")
    else:
        lines.append("- Raw artifacts appear centralized under data/raw/**.")
    if duplicates:
        lines.append("- Remove or consolidate duplicate raw files listed above to avoid confusion.")
    lines.append("- Enhance income/employment ingestion to cache raw API arrays and attach provenance (endpoint, variables, geography, retrieved_at, raw_saved_to).")
    lines.append("- Keep figures and analysis reading only persisted inputs; avoid any transient data in notebooks.")

    # Status
    lines.append("\n## Status\n")
    lines.append(f"Overall: {'PASS' if overall_ok else 'WARN/FAIL'}")

    out_dir = os.path.join(ROOT, 'data')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'provenance_audit_report.md')
    with open(out_path, 'w') as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote provenance audit report to {_rel(out_path)}")
    if not overall_ok:
        print("One or more critical checks failed; see report for details.")
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
