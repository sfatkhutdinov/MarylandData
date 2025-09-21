#!/usr/bin/env python3
"""
Analyze the actual Census data collected for ZIP 21076 (Hanover, MD)

This script examines real data without making assumptions about what should exist.
It discovers the actual demographic profile based on what the Census API returned.
"""

import json
import pandas as pd
from pathlib import Path

def load_discovered_data():
    """Load the raw discovered data"""
    data_path = Path('data/raw/zip_21076_discovered_data.json')
    with open(data_path, 'r') as f:
        return json.load(f)

def convert_census_value(value):
    """Convert Census values handling special codes and string numbers"""
    if value is None:
        return None
    if isinstance(value, str):
        if value == '0':
            return 0
        # Census error codes (actual from data)
        if value in ['-666666666', '-888888888', '-999999999']:
            return None  # Data not available/suppressed
        try:
            return int(value)
        except ValueError:
            return value
    return value

def analyze_basic_demographics(data):
    """Find and analyze basic demographic variables"""
    results = {}
    
    # Key demographic patterns from actual data
    key_patterns = {
        'Total Population': 'B01003_001E',
        'Median Household Income': 'B19013_001E', 
        'Median Home Value': 'B25077_001E',
        'Total Housing Units': 'B25001_001E',
        'Owner Occupied': 'B25003_002E',
        'Renter Occupied': 'B25003_003E'
    }
    
    for description, var_id in key_patterns.items():
        if var_id in data['data']:
            entry = data['data'][var_id]
            raw_value = entry['value']
            definition = entry.get('definition', 'No definition available')
            converted_value = convert_census_value(raw_value)
            results[description] = {
                'variable_id': var_id,
                'raw_value': raw_value,
                'converted_value': converted_value,
                'official_definition': definition
            }
    
    return results

def analyze_commuting_patterns(data):
    """Analyze actual commuting data from B08301 series"""
    commute_data = {}
    
    for var_id, entry in data['data'].items():
        if var_id.startswith('B08301'):
            raw_value = entry['value']
            definition = entry.get('definition', 'No definition available')
            converted_value = convert_census_value(raw_value)
            commute_data[var_id] = {
                'raw': raw_value,
                'converted': converted_value,
                'definition': definition
            }
    
    # Key commuting variables we found
    key_commute_vars = {
        'B08301_001E': 'Total Workers 16+',
        'B08301_010E': 'Public Transportation',
        'B08301_021E': 'Worked from Home',  # Corrected from walk
        'B08301_003E': 'Car/Truck/Van Alone',
        'B08301_004E': 'Car/Truck/Van Carpooled'
    }
    
    results = {}
    for var_id, description in key_commute_vars.items():
        if var_id in commute_data:
            results[description] = commute_data[var_id]
    
    return results

def analyze_income_distribution(data):
    """Analyze income distribution from B19001 series"""
    income_data = {}
    
    for var_id, entry in data['data'].items():
        if var_id.startswith('B19001'):
            raw_value = entry['value']
            definition = entry.get('definition', 'No definition available')
            converted_value = convert_census_value(raw_value)
            if converted_value is not None and isinstance(converted_value, int) and converted_value > 0:
                income_data[var_id] = {
                    'value': converted_value,
                    'definition': definition
                }
    
    return income_data

def analyze_age_distribution(data):
    """Analyze age distribution from B01001 series"""
    age_data = {}
    
    for var_id, entry in data['data'].items():
        if var_id.startswith('B01001'):
            raw_value = entry['value']
            definition = entry.get('definition', 'No definition available')
            converted_value = convert_census_value(raw_value)
            if converted_value is not None:
                age_data[var_id] = {
                    'value': converted_value,
                    'definition': definition
                }
    
    return age_data

def generate_summary_report(basic_demo, commute_data, income_data, age_data):
    """Generate a summary report of actual findings"""
    
    print("=" * 60)
    print("HANOVER, MD (ZIP 21076) - ACTUAL CENSUS DATA ANALYSIS")
    print("Source: 2023 ACS 5-Year Estimates")
    print("=" * 60)
    print()
    
    print("📊 BASIC DEMOGRAPHICS")
    print("-" * 40)
    for desc, info in basic_demo.items():
        value = info['converted_value']
        if value is not None:
            if 'Income' in desc or 'Value' in desc:
                print(f"{desc}: ${value:,}")
            else:
                print(f"{desc}: {value:,}")
        else:
            print(f"{desc}: Data not available ({info['raw_value']})")
    print()
    
    print("🚗 COMMUTING PATTERNS")  
    print("-" * 40)
    total_workers = None
    for desc, info in commute_data.items():
        value = info['converted']
        definition = info.get('definition', 'No definition')
        if value is not None:
            if desc == 'Total Workers 16+':
                total_workers = value
            print(f"{desc}: {value:,}")
            print(f"  Definition: {definition}")
            if total_workers and desc != 'Total Workers 16+' and value > 0:
                percentage = (value / total_workers) * 100
                print(f"  ({percentage:.1f}% of workers)")
        else:
            print(f"{desc}: Data not available")
            print(f"  Definition: {definition}")
        print()
    print()
    
    print("💰 INCOME INSIGHTS")
    print("-" * 40)
    if income_data:
        print(f"Income variables with data: {len(income_data)}")
        # Show a few examples
        sample_vars = list(income_data.items())[:5]
        for var_id, info in sample_vars:
            value = info['value']
            definition = info['definition']
            print(f"  {var_id}: {value:,}")
            print(f"    {definition}")
    else:
        print("No income distribution data available")
    print()
    
    print("👥 AGE DEMOGRAPHICS")
    print("-" * 40)
    if age_data:
        print(f"Age variables with data: {len(age_data)}")
        # Show total and key age groups
        if 'B01001_001E' in age_data:
            total_pop = age_data['B01001_001E']['value']
            definition = age_data['B01001_001E']['definition']
            print(f"  Total Population: {total_pop:,}")
            print(f"    {definition}")
    else:
        print("No age distribution data available")
    print()
    
    print("📋 DATA QUALITY NOTES")
    print("-" * 40)
    print("• Values of -666666666 indicate data not available/suppressed")
    print("• All numeric values returned as strings from Census API")
    print("• ZIP 21076 spans Howard and Anne Arundel Counties")
    print("• Analysis based on actual API responses, no assumptions")

def main():
    """Main analysis function"""
    print("Loading discovered Census data for ZIP 21076...")
    
    # Load the raw data
    data = load_discovered_data()
    print(f"Loaded {len(data['data'])} variables")
    
    # Analyze different aspects
    basic_demo = analyze_basic_demographics(data)
    commute_data = analyze_commuting_patterns(data)
    income_data = analyze_income_distribution(data)
    age_data = analyze_age_distribution(data)
    
    # Generate summary report
    generate_summary_report(basic_demo, commute_data, income_data, age_data)
    
    # Save analysis results
    analysis_results = {
        'basic_demographics': basic_demo,
        'commuting_patterns': commute_data,
        'income_data_count': len(income_data),
        'age_data_count': len(age_data),
        'analysis_timestamp': data['metadata']
    }
    
    output_path = Path('data/processed/zip_21076_analysis.json')
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"\n📁 Analysis saved to: {output_path}")

if __name__ == "__main__":
    main()