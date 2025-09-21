#!/usr/bin/env python3
"""
Parse the Maryland Department of Labor August 2025 employment news release
and persist verified metrics with full provenance.

Input: data/raw/mlraug2025.md (saved verbatim from MD Labor site)
Output: data/processed/mlraug2025.json with fields:
  {
    "source_url": str,
    "retrieved_at": str,
    "period": "2025-08",
    "highlights": {
        "jobs_change_total": int,
        "federal_jobs_change": int,
        "federal_jobs_change_ytd": int,
        "unemployment_rate": float,
        "national_unemployment_rate": float
    },
    "top_gainers": [ {"sector": str, "jobs_change": int}, ... ],
    "top_losers": [ {"sector": str, "jobs_change": int}, ... ]
  }

If the source file is missing or the expected phrases cannot be located,
the script exits with a non-zero code to prevent downstream hallucinations.
"""
import json
import os
import re
from datetime import datetime, timezone

RAW_PATH = os.path.join("data", "raw", "mlraug2025.md")
OUT_PATH = os.path.join("data", "processed", "mlraug2025.json")
SOURCE_URL = "https://www.labor.maryland.gov/whatsnews/mlraug2025.shtml"


def must_read_text(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required source missing: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_int(pattern: str, text: str, *, group: int = 1) -> int:
    m = re.search(pattern, text, flags=re.IGNORECASE)
    if not m:
        raise ValueError(f"Could not find integer using pattern: {pattern}")
    # remove commas and signs handled by int()
    return int(m.group(group).replace(",", ""))


def extract_float(pattern: str, text: str, *, group: int = 1) -> float:
    m = re.search(pattern, text, flags=re.IGNORECASE)
    if not m:
        raise ValueError(f"Could not find float using pattern: {pattern}")
    return float(m.group(group))


def extract_sector_changes(text: str, header: str) -> list:
    # Example line: "Construction (2,700 jobs); Accommodation and Food Services (1,400 jobs); ..."
    # We capture pairs of (sector, +/-N) under the header line.
    pattern_header = re.escape(header)
    m = re.search(pattern_header + r"\s*were:\s*(.+?)\.", text, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        raise ValueError(f"Could not locate sector list for: {header}")
    blob = m.group(1)
    entries = []
    for part in blob.split(";"):
        part = part.strip()
        sm = re.search(r"(.+?)\s*\(([\-\+]?[0-9,]+)\s+jobs?\)", part)
        if sm:
            sector = sm.group(1).strip()
            delta = int(sm.group(2).replace(",", ""))
            entries.append({"sector": sector, "jobs_change": delta})
    if not entries:
        raise ValueError("No sector entries parsed from header list")
    return entries


def main():
    text = must_read_text(RAW_PATH)
    retrieved_at = datetime.now(timezone.utc).isoformat()

    # Core metrics
    jobs_change_total = extract_int(r"workforce (?:decreased|declined) by\s+([\-\+]?[0-9,]+) jobs", text)
    federal_jobs_change = extract_int(r"loss of (?:another\s*)?([\-\+]?[0-9,]+) federal jobs in August", text)
    federal_jobs_change_ytd = extract_int(r"lost\s+([\-\+]?[0-9,]+) federal jobs since January\s*2025", text)
    unemployment_rate = extract_float(r"unemployment rate increased from\s*([0-9]\.[0-9])\s*percent to\s*([0-9]\.[0-9])\s*percent", text, group=2)
    national_unemployment_rate = extract_float(r"national rate \((?:[0-9]\.[0-9]) percent vs ([0-9]\.[0-9]) percent\)", text)

    top_gainers = extract_sector_changes(text, "The five sectors with the largest employment gains in August")
    top_losers = extract_sector_changes(text, "The five sectors with the largest estimated employment losses in August")

    out = {
        "source_url": SOURCE_URL,
        "retrieved_at": retrieved_at,
        "period": "2025-08",
        "highlights": {
            "jobs_change_total": jobs_change_total,
            "federal_jobs_change": federal_jobs_change,
            "federal_jobs_change_ytd": federal_jobs_change_ytd,
            "unemployment_rate": unemployment_rate,
            "national_unemployment_rate": national_unemployment_rate,
        },
        "top_gainers": top_gainers,
        "top_losers": top_losers,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Fail hard to avoid downstream hallucination
        import sys
        print(f"ERROR: {e}")
        sys.exit(1)
