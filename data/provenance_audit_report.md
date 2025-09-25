# Provenance Audit Report

Generated: 2025-09-25 00:02:19Z UTC

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
  • Income ingestion has provenance and raw cache: PASS (data/raw/census/acs5_2023_B19001_zcta21076_20250924T235242Z.json)
  • Employment ingestion has provenance and raw cache: PASS (data/raw/census/acs5_2023_C24010_zcta21076_20250924T235242Z.json)

### Raw file layout

- Raw files discovered: 18
  • No misplaced raw files detected
  • No duplicate raw artifacts detected

## Recommendations

- Raw artifacts appear centralized under data/raw/**.
- Keep figures and analysis reading only persisted inputs; avoid any transient data in notebooks.

## Status

Overall: PASS
