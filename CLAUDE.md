# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a community improvement analysis project for Hanover, MD focused on evidence-based methodology and transparent analysis. The project is currently undergoing a complete methodological rebuild due to flaws identified in the original analysis.

## Project Structure

```
├── .archive/                    # Original analysis files (methodological issues identified)
├── data/                        # All datasets and data collection
│   ├── raw/                     # Original, unmodified data with source documentation
│   ├── processed/               # Cleaned data with transformation documentation
│   └── external/                # Third-party datasets with licenses
├── analysis/                    # Statistical analysis and modeling
├── research/                    # Background research and literature
├── visuals/                     # Charts, maps, and visualizations
├── docs/                        # Technical documentation and reports
├── scripts/                     # Data collection and analysis scripts
├── PLAN.md                      # Main community improvement plan
├── TODO.md                      # Methodological issues and action items
└── README.md                    # Project structure overview
```

## Development Environment

- **Language**: Python 3.9+
- **Environment**: Virtual environment located in `.venv/`
- **Dependencies**: Managed via pip (no requirements.txt currently exists)

### Common Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install common data science packages (if needed)
pip install pandas numpy matplotlib seaborn requests jupyter

# Run Python scripts from project root
python scripts/[script_name].py
```

## Current Project Status

**CRITICAL**: The project is in a methodological rebuild phase. The `.archive/` directory contains the original analysis that had fundamental flaws:

- Hardcoded demographic values instead of actual data collection
- Fabricated benefit calculations without supporting research
- Unrealistic funding assumptions
- Geographic data misapplication
- Correlation/causation errors

## Data Standards

All new analysis must follow these principles:

1. **Data Sources**: Use official government datasets (Census API, county GIS data)
2. **Geographic Precision**: ZIP code 21076-specific data, not county-wide averages
3. **Cost Estimates**: Based on recent comparable projects with documentation
4. **Benefit Calculations**: Grounded in peer-reviewed research with uncertainty ranges
5. **Transparency**: All assumptions documented and sources cited

## Key Action Items

Current high-priority tasks (see TODO.md for complete list):

1. Implement Census API data collection for ZIP 21076
2. Gather Maryland DOT construction cost data
3. Research healthcare cost studies for community health centers
4. Calculate realistic transportation savings based on usage patterns
5. Analyze federal grant program success rates

## Analysis Architecture

The project follows a rigorous methodology:

- **data/raw/**: Unmodified source data with collection metadata
- **data/processed/**: Cleaned data with transformation documentation
- **analysis/**: Statistical tests, models, and validation
- **research/**: Literature review and case studies
- **visuals/**: Evidence-based visualizations with uncertainty indicators

## Important Notes

- Never use hardcoded demographic or economic values
- All cost estimates must reference comparable real projects
- Include uncertainty ranges for all projections
- Document data collection timestamps and methodologies
- Use conservative estimates and acknowledge limitations
- The goal is community benefit through rigorous, defensible analysis