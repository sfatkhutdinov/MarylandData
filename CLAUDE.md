# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a community improvement analysis project for Hanover, MD (ZIP 21076) undergoing a methodological rebuild. The `.archive/` directory contains original analysis with fundamental flaws that must not be replicated.

## Development Environment

- **Language**: Python 3.9+
- **Virtual Environment**: `.venv/` (activate with `source .venv/bin/activate`)
- **Dependencies**: Install as needed via pip (no requirements.txt exists)
- **Configuration**: Copy `.env.template` to `.env` and add API keys

### Essential API Keys

```bash
# Required for demographic data
CENSUS_API_KEY=your_key_here  # Get at: https://api.census.gov/data/key_signup.html

# Optional but recommended for employment data
BLS_API_KEY=your_key_here     # Register at: https://data.bls.gov/registrationEngine/
```

### Common Commands

```bash
# Activate environment and install core packages
source .venv/bin/activate
pip install pandas numpy matplotlib seaborn requests jupyter

# Run data collection scripts
python scripts/census_data_collector.py
python scripts/maryland_transportation_costs.py

# Create visualizations
python scripts/hanover_demographics_viz.py
```

## Data Architecture

### Geographic Scope
- **Primary Study Area**: ZIP Code 21076 (Hanover, MD)
- **Population**: ~28,000 (verify via Census API)
- **Counties**: Howard County (west), Anne Arundel County (east)

### Key Data Sources
```python
DATA_SOURCES = {
    'census_acs5': 'https://api.census.gov/data/2023/acs/acs5',
    'maryland_open_data': 'https://opendata.maryland.gov',
    'howard_county_gis': 'https://data.howardcountymd.gov',
    'anne_arundel_open': 'https://opendata.aacounty.org',
    'bls_employment': 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
}

# Essential ACS variables for ZIP 21076
CORE_VARIABLES = {
    'B01003_001E': 'Total population',
    'B19013_001E': 'Median household income',
    'B08301_010E': 'Public transportation commuters',
    'B08303_001E': 'Average commute time'
}
```

### Data Collection Patterns
```python
class HanoverDataCollector:
    def __init__(self):
        self.hanover_geo = {
            'zip_code': '21076',
            'zcta_code': '21076',
            'state_fips': '24',  # Maryland
            'counties': {
                'howard': {'state': '24', 'county': '027'},
                'anne_arundel': {'state': '24', 'county': '003'}
            }
        }

    def get_acs_data(self, variables, geography='zip code tabulation area:21076'):
        # Use Census API with proper error handling
        # Always document data collection timestamps
        # Include margin of error calculations
```

## Visualization Standards

```python
# Professional styling setup
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")  # Colorblind-friendly

# Required elements for all charts:
# 1. Error bars/confidence intervals
# 2. Data source attribution
# 3. Collection date/methodology notes
# 4. Conservative estimates with uncertainty ranges
```

## Critical Methodological Rules

1. **Geographic Precision**: ZIP code 21076-specific data only, never county averages
2. **No Hardcoded Values**: All data must come from official APIs with timestamps
3. **Employment Verification**: Cross-reference BLS, OES, and OPM data for all employment claims
4. **Conservative Estimates**: Include uncertainty ranges and acknowledge limitations
5. **Source Documentation**: Every data point requires collection methodology and timestamp
6. **Peer Review Grounding**: All analytical methods must reference published research

## Architecture Notes

- **data/raw/**: Unmodified API responses with collection metadata
- **data/processed/**: Cleaned datasets with transformation documentation
- **analysis/**: Statistical tests with uncertainty quantification
- **scripts/**: Automated data collection with error handling
- **visuals/**: Professional charts with source attribution and error bars

## Development Priorities

1. **Census API Implementation**: Demographic data collection for ZIP 21076
2. **Maryland DOT Data**: Construction cost benchmarks from state sources
3. **Employment Analysis**: BLS occupational statistics and federal employment data
4. **Literature Review**: Peer-reviewed community impact studies for methodology validation