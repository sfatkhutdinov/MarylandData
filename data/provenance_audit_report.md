# Provenance Audit Report

Generated: 2025-09-24 23:53:37Z UTC

## Checks

### Baseline (data/hanover_real_data.json)

- data/hanover_real_data.json exists: PASS
  • ACS block present with provenance: PASS
    – Referenced raw ACS file exists: PASS (data/raw/census/acs5_2023_zcta21076_20250924T235331Z.json)
  • Decennial block present with provenance: PASS
    – Referenced raw Decennial file exists: PASS (data/raw/census/decennial_2020_dhc_zcta21076_20250924T235332Z.json)
  • population_2023 matches raw B01003_001E: PASS
  • price_to_income_ratio consistent with median_home_value/median_income: PASS
  • vacancy_rate consistent with raw B25001/B25003: PASS

### Detailed (data/real_employment_income.json)

- data/real_employment_income.json exists: PASS
  • Contains income, employment, affordability blocks: PASS
  • Affordability provenance baseline path exists: PASS (data/hanover_real_data.json)

Notes:
- Raw API arrays for income/employment are not cached in data/raw; recommend enhancing ingestion to persist raw + provenance.

### Raw file layout

- Raw files discovered: 19
  • No misplaced raw files detected
  • Duplicate raw artifacts (identical content):
    – data/raw/census/acs5_2023_zcta21076_20250924T235331Z.json == data/raw/census/acs5_2023_zcta21076_20250924T235229Z.json

## Recommendations

- Raw artifacts appear centralized under data/raw/**.
- Remove or consolidate duplicate raw files listed above to avoid confusion.
- Enhance income/employment ingestion to cache raw API arrays and attach provenance (endpoint, variables, geography, retrieved_at, raw_saved_to).
- Keep figures and analysis reading only persisted inputs; avoid any transient data in notebooks.

## Status

Overall: PASS
