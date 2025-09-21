# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **streamlined community improvement analysis** for Hanover, MD (ZIP 21076). The project has been cleaned up to focus on a single authoritative README containing evidence-based recommendations for human-centered community development.

**Key Changes:** All working directories have been archived. The project now centers on the comprehensive analysis in `README.md` with MCP-enhanced data verification.

## Development Environment

- **Language**: Python 3.9+ (for any data collection scripts)
- **Virtual Environment**: `.venv/` (activate with `source .venv/bin/activate`)
- **Dependencies**: `pip install -r requirements.txt` (if needed for data collection)
- **Configuration**: Copy `.env.template` to `.env` and add API keys for data verification

### Essential API Keys

```bash
# Required for demographic verification
CENSUS_API_KEY=your_key_here  # Get at: https://api.census.gov/data/key_signup.html

# Optional for employment data verification
BLS_API_KEY=your_key_here     # Register at: https://data.bls.gov/registrationEngine/
```

### Project Commands

```bash
# Setup (if data collection needed)
source .venv/bin/activate
pip install -r requirements.txt

# Primary deliverable is README.md - no regular scripts to run
# All analysis results are documented in the main README

# MCP server verification (documented in .mcp.json)
# Use MCP tools to verify claims in README.md against authoritative sources
```

## Project Architecture

### Current Structure (Streamlined)
- **`.archive/`**: All previous working files, scripts, and directories
- **`README.md`**: **PRIMARY DELIVERABLE** - Complete community improvement analysis
- **`.mcp.json`**: MCP server configuration for data verification
- **`CLAUDE.md`**: This guidance file
- **`.env.template`**: Environment configuration template
- **`requirements.txt`**: Python dependencies (if needed)

### Key Insights Already Documented

The README.md contains a complete evidence-based analysis including:

1. **Demographics**: Population 22,299-28,089, $143,409 median income, 63.5% STEM educated
2. **Growth Challenge**: 31.6% population increase by 2025, 2,627 housing unit deficit by 2030
3. **Four Priority Areas**: Housing, Transportation, Community Services, Economic Equity
4. **Implementation Framework**: Four-phase approach with specific timelines
5. **Data Verification**: Multi-source verification documented with methodological transparency

## MCP Integration for Data Verification

The project uses Model Context Protocol servers (`.mcp.json`) to maintain data integrity:

### Core Verification Servers
- **wikipedia**: Verify demographic facts and community context
- **datagov**: Cross-reference federal datasets
- **web-search**: Check current developments and policy updates
- **memory**: Track research findings and contradictions
- **sequential-thinking**: Plan complex verification workflows
- **opengov**: Access Maryland state data directly

### MCP Usage for README Maintenance

**When updating README.md claims:**
1. **Verify Demographics**: Use Wikipedia and web search to confirm population/income data
2. **Check Current Projects**: Use web search for infrastructure project status updates
3. **Cross-Reference Data**: Use opengov and datagov for official statistics
4. **Document Sources**: Use memory to track verification steps and data quality
5. **Plan Updates**: Use sequential-thinking for systematic analysis updates

### Example Verification Workflow
```python
# Before updating any demographic claim in README.md:
# 1. Use web search MCP to check for recent Census releases
# 2. Use Wikipedia MCP to verify community boundaries/characteristics
# 3. Use opengov MCP to check Maryland state data for updates
# 4. Use memory MCP to document all verification steps
# 5. Update README.md only with multi-source verified data
```

## Critical Guidelines

1. **README.md is the Primary Deliverable**: All analysis, recommendations, and findings are in this single document
2. **Evidence-Based Claims Only**: Every statistic must be verifiable through MCP servers
3. **Anti-Hallucination Protocol**: Use minimum 2 authoritative sources for all claims
4. **Current Context**: Always incorporate 2024-2025 policy and project updates
5. **Community-Centered**: Focus on human-centered development that serves all residents
6. **Methodological Transparency**: Document all data sources and verification steps

## Archive Reference

Previous work is preserved in `.archive/` including:
- Original data collection scripts (`scripts/`)
- Raw and processed datasets (`data/`)
- Exploratory analysis (`analysis/`)
- Research materials (`research/`, `docs/`)
- Planning documents (`PLAN.md`, `TODO.md`)

**Important**: Use archived materials for reference only. Do not replicate methodological approaches from `.archive/` - the current streamlined approach in README.md represents the refined analysis.

## Development Priorities

1. **README.md Maintenance**: Keep the community improvement analysis current with latest data
2. **Data Verification**: Regularly verify claims using MCP servers
3. **Policy Updates**: Monitor for new infrastructure projects, zoning changes, demographic updates
4. **Community Feedback**: Update recommendations based on implementation progress

## Success Metrics

- All demographic claims in README.md verified against 2+ authoritative sources
- Implementation framework reflects current 2024-2025 policy context
- Recommendations are actionable and tied to specific data sources
- Analysis serves as replicable template for similar suburban communities

This streamlined approach prioritizes a single, authoritative analysis document over scattered working files, while maintaining rigorous data verification through MCP integration.