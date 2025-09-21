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
            'mdot_data': 'https://opendata.maryland.gov/browse?category=Transportation',
            
            # County APIs
            'howard_county_gis': 'https://data.howardcountymd.gov',
            'anne_arundel_open': 'https://opendata.aacounty.org',
            
            # Federal Grant Data
            'build_grants': 'https://www.transportation.gov/BUILDgrants/awarded-projects',
            'ss4a_grants': 'https://www.transportation.gov/grants/ss4a',
            
            # Employment Data (for comprehensive occupational analysis)
            'bls_qcew': 'https://api.bls.gov/publicAPI/v2/timeseries/data/',
            'bls_oes': 'https://www.bls.gov/oes/tables.htm',  # Occupational Employment Statistics
            'opm_fedscope': 'https://www.fedscope.opm.gov/',  # Federal employment by location
            'usajobs_api': 'https://developer.usajobs.gov/'   # Federal job postings
        }
        
        # Geographic identifiers for ZIP 21076
        self.hanover_geo = {
            'zip_code': '21076',
            'zcta_code': '21076',  # ZIP Code Tabulation Area
            'counties': {
                'howard': {'state': '24', 'county': '027'},
                'anne_arundel': {'state': '24', 'county': '003'}
            },
            'state_fips': '24',  # Maryland
            'estimated_population': 28089  # Verify via API
        }

    def get_acs_demographics(self, variables, geography='zip code tabulation area:21076'):
        """
        Get ACS data for specific variables and geography
        Example variables:
        - B01003_001E: Total population
        - B19013_001E: Median household income
        - B25077_001E: Median home value
        - B08301_010E: Public transportation commuters
        """
        url = f"{self.data_sources['acs5_detailed']}"
        params = {
            'get': ','.join(variables),
            'for': geography,
            'key': self.api_key
        }
        # API call implementation...
```

### Essential ACS Variables for Hanover Analysis
```python
HANOVER_KEY_VARIABLES = {
    'demographics': {
        'B01003_001E': 'Total population',
        'B01002_001E': 'Median age',
        'B19013_001E': 'Median household income',
        'B25077_001E': 'Median home value',
        'B25003_002E': 'Owner-occupied housing units',
        'B25003_003E': 'Renter-occupied housing units'
    },
    'transportation': {
        'B08301_010E': 'Public transportation commuters',
        'B08301_021E': 'Walk to work',
        'B08301_016E': 'Bicycle commuters',
        'B08303_001E': 'Average commute time'
    },
    'economic': {
        'B23025_005E': 'Unemployed population',
        'B15003_022E': "Bachelor's degree",
        'B15003_023E': "Master's degree",
        'C24010_038E': 'Computer/mathematical occupations'
    },
    'employment_validation': {
        # Use BLS QCEW for actual employment by industry in Howard/Anne Arundel Counties
        # Use OES data for occupational employment and wages across ALL sectors
        # Cross-reference with OPM FedScope for federal vs private employment balance
        'validate_all_claims': 'NEVER assume employment demographics without comprehensive BLS/OPM data'
    }
}
```

### Visualization Standards for Beautiful, Meaningful Charts
```python
# Professional visualization setup
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set consistent, beautiful styling
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")  # Colorblind-friendly, professional palette

class HanoverVisualizer:
    def __init__(self):
        # Professional color schemes
        self.colors = {
            'primary': '#2E86AB',      # Professional blue
            'secondary': '#A23B72',    # Muted magenta  
            'accent': '#F18F01',       # Warm orange
            'neutral': '#C73E1D',      # Deep red
            'success': '#6A994E',      # Natural green
            'warning': '#F77F00',      # Amber
            'info': '#577590',         # Steel blue
            'light_gray': '#F8F9FA',   # Background
            'dark_gray': '#495057'     # Text
        }
        
        # Typography settings
        self.fonts = {
            'title': {'fontsize': 16, 'fontweight': 'bold', 'color': self.colors['dark_gray']},
            'subtitle': {'fontsize': 12, 'fontweight': 'medium', 'color': self.colors['dark_gray']},
            'body': {'fontsize': 10, 'color': self.colors['dark_gray']},
            'caption': {'fontsize': 8, 'style': 'italic', 'color': self.colors['info']}
        }
        
    def create_uncertainty_chart(self, estimates, margins_of_error, labels):
        """
        Create beautiful charts with error bars showing data uncertainty
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Main bars with error bars
        bars = ax.bar(labels, estimates, 
                     color=self.colors['primary'], 
                     alpha=0.8,
                     edgecolor=self.colors['dark_gray'],
                     linewidth=0.5)
        
        # Add error bars
        ax.errorbar(labels, estimates, yerr=margins_of_error,
                   fmt='none', capsize=4, capthick=1,
                   ecolor=self.colors['neutral'], alpha=0.7)
        
        # Beautiful formatting
        ax.set_title('Title with Data Source & Date', **self.fonts['title'], pad=20)
        ax.set_ylabel('Y-axis Label with Units', **self.fonts['subtitle'])
        
        # Add uncertainty note
        ax.text(0.02, 0.98, '±Error bars show 90% confidence intervals', 
               transform=ax.transAxes, **self.fonts['caption'],
               verticalalignment='top')
        
        # Clean styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig, ax
        
    def create_comparison_chart(self, hanover_data, comparison_data, metric_name):
        """
        Create meaningful comparison charts (Hanover vs County vs State vs National)
        """
        locations = ['Hanover\n(ZIP 21076)', 'Howard County', 'Maryland', 'United States']
        values = [hanover_data, comparison_data['county'], 
                 comparison_data['state'], comparison_data['national']]
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Color coding: highlight Hanover, neutral for comparisons
        colors = [self.colors['primary'], self.colors['secondary'], 
                 self.colors['accent'], self.colors['neutral']]
        
        bars = ax.bar(locations, values, color=colors, alpha=0.8)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'{value:,.0f}', ha='center', va='bottom', **self.fonts['body'])
        
        # Professional title with context
        ax.set_title(f'{metric_name}\nComparison Across Geographic Levels', 
                    **self.fonts['title'], pad=20)
        
        # Source attribution (CRITICAL for credibility)
        source_text = 'Source: U.S. Census Bureau, 2019-2023 ACS 5-Year Estimates'
        ax.text(0.02, 0.02, source_text, transform=ax.transAxes, 
               **self.fonts['caption'])
        
        # Clean, professional styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylabel(f'{metric_name}', **self.fonts['subtitle'])
        plt.xticks(rotation=0, **self.fonts['body'])
        plt.tight_layout()
        return fig, ax

# Key visualization principles:
# 1. Always include uncertainty (error bars, confidence intervals)
# 2. Use colorblind-friendly palettes (Set2, viridis, colorbrewer)
# 3. Add data source attribution on every chart
# 4. Include sample sizes and methodology notes
# 5. Show ranges, not just point estimates
# 6. Use consistent typography hierarchy
# 7. Highlight key findings with color, not emotional manipulation
```

## Immediate Development Priorities

### Phase 1: Data Foundation
1. Implement Census API collection for ZIP 21076 demographics
2. Set up Maryland DOT construction cost database
3. Create data validation pipelines with error handling

### Phase 2: Analysis Infrastructure  
1. Literature review methodology for community impact studies
2. Statistical analysis templates with uncertainty quantification
3. Transparent cost-benefit calculation frameworks

## Critical Methodological Rules

1. **Geographic Precision**: Use ZIP code or Census block group data, never county-wide averages
2. **Source Documentation**: Every data point must have collection timestamp and methodology
3. **Employment Claims**: NEVER assume employment demographics without comprehensive BLS verification
4. **Conservative Estimates**: Err on the side of caution for all projections
5. **Peer Review**: All analytical methods must be grounded in published research
6. **Transparency**: All assumptions documented, limitations acknowledged

## Integration Points

- **Census Bureau APIs** for demographic data
  - API Key required: https://api.census.gov/data/key_signup.html
  - Primary endpoint: `https://api.census.gov/data/2023/acs/acs5`
  - Geography syntax: `zip code tabulation area:21076` (code 860)
  - Variables documentation: https://api.census.gov/data/2023/acs/acs5/variables.json

- **Maryland Open Data Portal** for state-level datasets
  - Base URL: https://opendata.maryland.gov  
  - Transportation category for MDOT construction costs
  - Socrata API for programmatic access

- **Howard County GIS** for local western context
  - Base URL: https://data.howardcountymd.gov
  - Interactive map and My Neighborhood tools
  - Creative Commons Attribution 4.0 licensed data

- **Anne Arundel County Open Data** for local eastern context  
  - Base URL: https://opendata.aacounty.org
  - County-specific infrastructure and demographic data

- **Federal Grant Databases** for realistic funding scenarios
  - RAISE/BUILD grants: https://www.transportation.gov/BUILDgrants/awarded-projects
  - Safe Streets and Roads for All (SS4A): https://www.transportation.gov/grants/ss4a
  - Historical success rates and funding levels available

## Common Patterns from Archive Analysis

The archived code shows consistent patterns for:
- Class-based data collectors with multiple API endpoints
- Matplotlib/seaborn visualization with professional styling
- JSON data structures for demographic breakdowns
- Comparative analysis (Hanover vs. Maryland vs. National)

**Remember**: The archive represents what NOT to do methodologically, but shows useful code structure patterns for data collection and visualization.