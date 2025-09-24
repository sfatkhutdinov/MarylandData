# GitHub Copilot Instructions

## CRITICAL: Memory Management Required

**🧠 MANDATORY: Use memory MCP for ALL sessions**
- ALWAYS call `mcp_memory_search_nodes` at session start to retrieve previous context
- ALWAYS call `mcp_memory_add_observations` when discovering new patterns or making decisions
- ALWAYS call `mcp_memory_create_entities` to store project context, decisions, and rationale
- NEVER proceed without establishing memory context of prior work and methodological decisions

## Project Overview

This is a **methodological rebuild** of a community improvement analysis for Hanover, MD (ZIP 21076). The project is currently in active reconstruction due to fundamental flaws identified in the original analysis (archived in `.archive/`).

## Critical Context: Data Integrity Requirements

**⚠️ NEVER use hardcoded demographic or economic values**. The original analysis was invalidated because it contained fabricated data. All new work must:

- Use real Census API data for ZIP 21076 specifically (not county-wide data)
- Reference actual Maryland DOT construction costs with documentation
- Ground benefit calculations in peer-reviewed research with cited sources
- Include uncertainty ranges and acknowledge limitations
- Document all data collection methodologies and timestamps

## Project Architecture

### Directory Structure & Purpose
- `data/raw/` - Original datasets with source documentation (currently empty - needs population)
- `data/processed/` - Cleaned data with transformation logs 
- `analysis/` - Statistical analysis with reproducible methodology
- `scripts/` - Data collection and processing automation
- `research/` - Literature review and case studies
- `.archive/` - Original flawed analysis for reference only

### Key Geographic Identifiers
- **Primary Study Area**: ZIP Code 21076 (Hanover, MD)
- **Counties**: Howard County (west), Anne Arundel County (east)
- **Population**: ~28,000 (verify via Census API)
- **Geographic Context**: Suburban community in Baltimore-DC metro area

## Development Standards

### Session Management Protocol
**🧠 REQUIRED MEMORY WORKFLOW:**
1. **Session Start**: `mcp_memory_search_nodes` to retrieve project context
2. **During Work**: `mcp_memory_add_observations` for all decisions and discoveries
3. **Before Ending**: `mcp_memory_create_entities` for new components or insights
4. **NEVER**: Work without memory context - methodological decisions must persist

### Python Environment
- **Python 3.9+** required
- **Virtual Environment**: Use `.venv/` (not currently set up)
- **Dependencies**: Install as needed - no requirements.txt exists yet
- **Common imports**: `pandas`, `numpy`, `matplotlib`, `seaborn`, `requests` for Census/GIS APIs

### Data Collection Patterns & APIs
```python
# Complete API structure for Hanover analysis
class HanoverDataCollector:
    def __init__(self):
        self.api_key = None  # Get from https://api.census.gov/data/key_signup.html
        self.data_sources = {
            # Primary Census APIs
            'acs5_detailed': 'https://api.census.gov/data/2023/acs/acs5',
            'acs5_subject': 'https://api.census.gov/data/2023/acs/acs5/subject',
            'acs5_profile': 'https://api.census.gov/data/2023/acs/acs5/profile',
            
            # Maryland State Data
            'maryland_open_data': 'https://opendata.maryland.gov',
            ````instructions
            # GitHub Copilot Instructions (MarylandData)

            Last updated: 2025-09-24

            ## Mission & Guardrails
            - This repo performs a methodological, evidence-only analysis for Hanover, MD (ZCTA 21076).
            - Do not fabricate values. Use persisted sources only. If a value isn’t in data/raw or produced by scripts, acquire it via an API and save it with provenance before analysis.
            - Use ZIP code tabulation area (ZCTA) 21076, not county-wide stand-ins, unless explicitly marked and sourced as comparisons.
            - Always include sources, retrieval timestamps, and uncertainty where applicable; avoid introducing “approximate” benchmarks without persisted provenance.

            ## MCP Memory Protocol (Required for AI agents)
            - At session start: call memory search to load prior context (decisions, data sources).
            - During work: add observations for key choices, edge cases, and provenance decisions.
            - Before ending: create entities for new scripts, datasets, or methods with rationale.
            - Goal: retain methodological decisions across sessions and prevent re‑introducing fabricated data.

            ## Repo Anatomy (what matters)
            - Top-level runners:
              - collect_hanover_data.py: pulls ACS 2023 and 2020 Decennial for ZCTA 21076, caches raw under data/raw/census, writes data/hanover_real_data.json and data/hanover_metrics.csv. Requires CENSUS_API_KEY (.env; python‑dotenv).
              - get_real_employment_data.py: pulls income distribution (B19001) and occupations (C24010), computes affordability using 30% rule and a documented PITI heuristic, writes data/real_employment_income.json.
              - scripts/ingest_md_labor_release.py: parses data/raw/mlraug2025.md and writes data/processed/mlraug2025.json; fails hard if phrases aren’t found. Used as context in visuals.
              - real_hanover_analysis.py: fail‑fast if required files missing, then generates figures in data/ using only persisted inputs.
              - create_visualizations.py: additional charts; replace any placeholders with persisted, sourced values before extending.
            - Data layout: data/raw/** (verbatim sources), data/processed/** (parsed JSON with provenance), data/*.json, *.csv (analysis outputs), analysis/hanover_current_state.ipynb (notebook exploration).

            ## Environment & Keys
            - Python 3.9+. Use .venv and requirements.txt. Load API keys from .env via python‑dotenv.
            - Required: CENSUS_API_KEY. Optional: others (e.g., BLS) if you wire new ingestion.

            ## Concrete Patterns (follow these from code)
            - ACS requests: geography='zip code tabulation area:21076'; convert sentinel values ('-666…') to None; coerce numerics robustly.
            - Raw caching + provenance: save raw API arrays to data/raw/census with timestamped filenames (e.g., acs5_2023_zcta21076_YYYYMMDDTHHMMSSZ.json); record endpoint, variables, geography, retrieved_at, raw_saved_to; never persist API keys.
            - Calculations: compute vacancy rate, price-to-income ratio, college+ shares from explicit variables; affordability uses 30% rule; document heuristics inline.
            - Visualization hygiene: use seaborn Set2; avoid bare '$' in Matplotlib strings (use 'USD '); save figures under data/; include source footers with URLs and retrieval timestamps when available.
            - Fail-fast runners: real_hanover_analysis.py exits non‑zero if required inputs missing and prints remediation steps; keep this pattern for any new pipeline stage.

            ## Typical Workflow (end-to-end)
            1) Setup env (.venv) and install requirements; add CENSUS_API_KEY to .env.
            2) Run collect_hanover_data.py (creates data/hanover_real_data.json, data/hanover_metrics.csv and caches raw census files).
            3) Run get_real_employment_data.py (creates data/real_employment_income.json).
            4) Save MD Labor release verbatim to data/raw/mlraug2025.md, then run scripts/ingest_md_labor_release.py (creates data/processed/mlraug2025.json or fails clearly).
            5) Run real_hanover_analysis.py to generate evidence‑sourced figures in data/.
            6) Use create_visualizations.py only with persisted, sourced inputs; remove or replace any placeholder comparisons with archived sources.

            ## Extension Points (do, but document)
            - If adding MDOT construction costs or housing authorizations, ingest via Maryland Open Data/Socrata, save raw + processed with timestamps, and cite dataset IDs. Do not hardcode “benchmarks”.
            - When adding comparisons (county/state/national), persist those sources alongside Hanover artifacts and attribute them on charts.

            ## Anti‑hallucination checklist
            - Is every number traceable to data/raw or a reproducible script? If not, ingest and persist first.
            - Does each figure include source text and retrieval timestamp when available?
            - Are any ACS variables or geographies ambiguous? Verify against Census variables.json and use ZCTA 21076 explicitly.

            Key files to consult: README.md (guardrails and workflow), collect_hanover_data.py, get_real_employment_data.py, scripts/ingest_md_labor_release.py, real_hanover_analysis.py, requirements.txt.
            ````