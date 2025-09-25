#!/usr/bin/env python3
"""
Get REAL employment and income data for Hanover
Stop making assumptions about who lives here and what they do
"""

import requests
import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _save_raw(payload, out_dir: str, label: str) -> str:
    _ensure_dir(out_dir)
    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    fname = f"{label}_{ts}.json"
    fpath = os.path.join(out_dir, fname)
    with open(fpath, 'w') as f:
        json.dump(payload, f, indent=2)
    return fpath

def get_detailed_income_distribution():
    """Get actual income distribution, not made-up brackets"""
    api_key = os.getenv('CENSUS_API_KEY')
    if not api_key:
        print("ERROR: Need CENSUS_API_KEY")
        return None

    base_url = 'https://api.census.gov/data/2023/acs/acs5'

    # ALL income distribution variables - let's see the real picture
    income_variables = {
        'B19001_001E': 'Total Households',
        'B19001_002E': 'Less than $10,000',
        'B19001_003E': '$10,000 to $14,999',
        'B19001_004E': '$15,000 to $19,999',
        'B19001_005E': '$20,000 to $24,999',
        'B19001_006E': '$25,000 to $29,999',
        'B19001_007E': '$30,000 to $34,999',
        'B19001_008E': '$35,000 to $39,999',
        'B19001_009E': '$40,000 to $44,999',
        'B19001_010E': '$45,000 to $49,999',
        'B19001_011E': '$50,000 to $59,999',
        'B19001_012E': '$60,000 to $74,999',
        'B19001_013E': '$75,000 to $99,999',
        'B19001_014E': '$100,000 to $124,999',
        'B19001_015E': '$125,000 to $149,999',
        'B19001_016E': '$150,000 to $199,999',
        'B19001_017E': '$200,000 or more'
    }

    params = {
        'get': ','.join(income_variables.keys()),
        'for': 'zip code tabulation area:21076',
        'key': api_key
    }

    try:
        response = requests.get(base_url, params=params, timeout=int(os.getenv('API_TIMEOUT', '30')))
        response.raise_for_status()
        data = response.json()

        if not data or len(data) < 2:
            return None

        headers = data[0]
        values = data[1]

        results = {}
        for i, header in enumerate(headers):
            if header in income_variables and i < len(values):
                raw_value = values[i]
                try:
                    if raw_value in ['-666666666', '-888888888', '-999999999', None]:
                        converted_value = None
                    else:
                        converted_value = int(raw_value)
                except (ValueError, TypeError):
                    converted_value = raw_value

                results[header] = {
                    'description': income_variables[header],
                    'value': converted_value
                }

        # Save raw and provenance
        raw_dir = os.path.join('data', 'raw', 'census')
        saved_path = _save_raw(data, raw_dir, 'acs5_2023_B19001_zcta21076')
        provenance = {
            'endpoint': base_url,
            'year': 2023,
            'variables': list(income_variables.keys()),
            'geography': 'zip code tabulation area:21076',
            'retrieved_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'raw_saved_to': saved_path
        }

        return {'data': results, 'provenance': provenance}

    except Exception as e:
        print(f"ERROR: {e}")
        return None

def get_employment_by_industry():
    """Get actual employment data - what do people actually do for work?"""
    api_key = os.getenv('CENSUS_API_KEY')
    if not api_key:
        return None

    base_url = 'https://api.census.gov/data/2023/acs/acs5'

    # Employment by industry - let's see reality
    employment_variables = {
        'C24010_001E': 'Total Employed',
        'C24010_002E': 'Management, business, science, and arts',
        'C24010_003E': 'Service occupations',
        'C24010_004E': 'Sales and office occupations',
        'C24010_005E': 'Natural resources, construction, maintenance',
        'C24010_006E': 'Production, transportation, material moving'
    }

    params = {
        'get': ','.join(employment_variables.keys()),
        'for': 'zip code tabulation area:21076',
        'key': api_key
    }

    try:
        response = requests.get(base_url, params=params, timeout=int(os.getenv('API_TIMEOUT', '30')))
        response.raise_for_status()
        data = response.json()

        if not data or len(data) < 2:
            return None

        headers = data[0]
        values = data[1]

        results = {}
        for i, header in enumerate(headers):
            if header in employment_variables and i < len(values):
                raw_value = values[i]
                try:
                    if raw_value in ['-666666666', '-888888888', '-999999999', None]:
                        converted_value = None
                    else:
                        converted_value = int(raw_value)
                except (ValueError, TypeError):
                    converted_value = raw_value

                results[header] = {
                    'description': employment_variables[header],
                    'value': converted_value
                }

        # Save raw and provenance
        raw_dir = os.path.join('data', 'raw', 'census')
        saved_path = _save_raw(data, raw_dir, 'acs5_2023_C24010_zcta21076')
        provenance = {
            'endpoint': base_url,
            'year': 2023,
            'variables': list(employment_variables.keys()),
            'geography': 'zip code tabulation area:21076',
            'retrieved_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'raw_saved_to': saved_path
        }

        return {'data': results, 'provenance': provenance}

    except Exception as e:
        print(f"ERROR: {e}")
        return None

def analyze_real_affordability(income_data, baseline_metrics_path: str = os.path.join('data', 'hanover_real_data.json')):
    """Calculate affordability using real income distribution and dynamic housing costs.

    Derives required annual income using the 30% rule based on:
    - ACS median gross rent (B25064_001E) if available (rent scenario)
    - Mortgage affordability for median home value (baseline metrics) using a simple heuristic:
      assume PITI ~ 0.006 of home value per month (approx 7.2% annual of value / 12) if explicit
      mortgage terms are not modeled. This remains a heuristic and is documented.
    """
    if not income_data:
        return None

    median_home_value = None
    median_gross_rent = None
    if os.path.exists(baseline_metrics_path):
        try:
            with open(baseline_metrics_path, 'r') as f:
                baseline = json.load(f)
                bmetrics = baseline.get('calculated_metrics', {})
                median_home_value = bmetrics.get('median_home_value')
                median_gross_rent = bmetrics.get('median_gross_rent')
        except Exception:
            pass

    # Determine monthly housing cost proxies
    monthly_rent = median_gross_rent if isinstance(median_gross_rent, (int, float)) else None
    monthly_piti = None
    if isinstance(median_home_value, (int, float)):
        # Heuristic: monthly PITI ~ 0.006 * home value (documented approximation)
        monthly_piti = 0.006 * median_home_value

    # Choose the larger of rent vs. mortgage proxy to set a conservative threshold
    monthly_housing_cost = None
    if monthly_rent and monthly_piti:
        monthly_housing_cost = max(monthly_rent, monthly_piti)
    elif monthly_rent:
        monthly_housing_cost = monthly_rent
    elif monthly_piti:
        monthly_housing_cost = monthly_piti

    # Fallback if neither available (should not happen once baseline is generated)
    if monthly_housing_cost is None:
        return None

    required_annual_income = monthly_housing_cost * 12 / 0.30  # 30% rule

    # Support both legacy shape (mapping) and new shape ({data, provenance})
    _income_block = income_data.get('data', income_data) if isinstance(income_data, dict) else {}
    total_households = _income_block.get('B19001_001E', {}).get('value')
    if not total_households:
        return None

    can_afford = 0
    cannot_afford = 0
    income_breakdown = {}

    # Calculate based on actual income distribution
    income_brackets = [
        ('B19001_002E', 'Less than $10,000', 10000),
        ('B19001_003E', '$10,000 to $14,999', 14999),
        ('B19001_004E', '$15,000 to $19,999', 19999),
        ('B19001_005E', '$20,000 to $24,999', 24999),
        ('B19001_006E', '$25,000 to $29,999', 29999),
        ('B19001_007E', '$30,000 to $34,999', 34999),
        ('B19001_008E', '$35,000 to $39,999', 39999),
        ('B19001_009E', '$40,000 to $44,999', 44999),
        ('B19001_010E', '$45,000 to $49,999', 49999),
        ('B19001_011E', '$50,000 to $59,999', 59999),
        ('B19001_012E', '$60,000 to $74,999', 74999),
        ('B19001_013E', '$75,000 to $99,999', 99999),
        ('B19001_014E', '$100,000 to $124,999', 124999),
        ('B19001_015E', '$125,000 to $149,999', 149999),
        ('B19001_016E', '$150,000 to $199,999', 199999),
        ('B19001_017E', '$200,000 or more', 300000)  # Conservative estimate
    ]

    for var_id, description, max_income in income_brackets:
        households = _income_block.get(var_id, {}).get('value', 0) or 0

        if households > 0:
            income_breakdown[description] = {
                'households': households,
                'percentage': (households / total_households) * 100
            }

        if max_income >= required_annual_income:
            can_afford += households
        else:
            cannot_afford += households

    return {
        'required_income': required_annual_income,
        'can_afford': can_afford,
        'cannot_afford': cannot_afford,
        'can_afford_percentage': (can_afford / total_households) * 100,
        'cannot_afford_percentage': (cannot_afford / total_households) * 100,
        'income_breakdown': income_breakdown,
        'total_households': total_households,
        'provenance': {
            'method': '30% income rule using ACS median gross rent and/or median home value PITI heuristic',
            'median_home_value_used': median_home_value,
            'median_gross_rent_used': median_gross_rent,
            'baseline_metrics_path': baseline_metrics_path
        }
    }

def main():
    """Get real employment and income data"""
    print("GETTING REAL EMPLOYMENT & INCOME DATA")
    print("=" * 50)

    print("\n1. Getting detailed income distribution...")
    income_data = get_detailed_income_distribution()

    print("\n2. Getting employment by industry...")
    employment_data = get_employment_by_industry()

    print("\n3. Calculating real affordability...")
    affordability = analyze_real_affordability(income_data)

    # Save results
    # For backward compatibility, provide flat mappings to analysis code
    income_payload = income_data['data'] if isinstance(income_data, dict) and 'data' in income_data else income_data
    employment_payload = employment_data['data'] if isinstance(employment_data, dict) and 'data' in employment_data else employment_data

    results = {
        'income_distribution': income_payload,
        'employment_by_industry': employment_payload,
        'affordability_analysis': affordability,
        # Attach provenance for transparency
        'income_provenance': income_data.get('provenance') if isinstance(income_data, dict) else None,
        'employment_provenance': employment_data.get('provenance') if isinstance(employment_data, dict) else None
    }

    os.makedirs('data', exist_ok=True)
    with open('data/real_employment_income.json', 'w') as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("\n" + "=" * 50)
    print("REAL DATA SUMMARY")
    print("=" * 50)

    if employment_payload:
        total_employed = employment_payload.get('C24010_001E', {}).get('value')
        if total_employed:
            print(f"\nEMPLOYMENT BY OCCUPATION:")
            for var_id, data in employment_payload.items():
                if var_id != 'C24010_001E' and data.get('value'):
                    percentage = (data['value'] / total_employed) * 100
                    print(f"  {data['description']}: {data['value']:,} ({percentage:.1f}%)")

    if affordability:
        print(f"\nHOUSING AFFORDABILITY (Real Calculation):")
        print(f"  Required income for median home: ${affordability['required_income']:,.0f}")
        print(f"  Households who CAN afford: {affordability['can_afford_percentage']:.1f}%")
        print(f"  Households who CANNOT afford: {affordability['cannot_afford_percentage']:.1f}%")

        print(f"\nINCOME DISTRIBUTION (Real Data):")
        for description, data in affordability['income_breakdown'].items():
            if data['households'] > 0:
                print(f"  {description}: {data['households']} households ({data['percentage']:.1f}%)")

    print(f"\nSaved to: data/real_employment_income.json")
    print("\nNow we know who actually lives here and what they can afford.")

if __name__ == "__main__":
    main()