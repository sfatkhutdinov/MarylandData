#!/usr/bin/env python3
"""
Real Data Collection for Hanover, MD (ZIP 21076)
Collects actual Census and government data for rigorous analysis
"""

import requests
import json
import os
import hashlib
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _save_raw(payload, out_dir: str, label: str) -> str:
    _ensure_dir(out_dir)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    fname = f"{label}_{ts}.json"
    fpath = os.path.join(out_dir, fname)
    with open(fpath, 'w') as f:
        json.dump(payload, f, indent=2)
    return fpath


def get_census_acs5(year: int = 2023):
    """Get ACS 5-year data for ZIP 21076 with provenance and raw caching."""
    api_key = os.getenv('CENSUS_API_KEY')
    if not api_key:
        print("ERROR: Need CENSUS_API_KEY in .env file")
        print("Get one at: https://api.census.gov/data/key_signup.html")
        return None

    base_url = f'https://api.census.gov/data/{year}/acs/acs5'

    # Core variables for analysis (add median gross rent)
    variables = {
        'B01003_001E': 'Total Population',
        'B19013_001E': 'Median Household Income',
        'B25077_001E': 'Median Home Value',
        'B25064_001E': 'Median Gross Rent',
        'B25001_001E': 'Total Housing Units',
        'B25003_002E': 'Owner Occupied Housing',
        'B25003_003E': 'Renter Occupied Housing',
        'B25004_001E': 'Vacancy Status Total',
        'B08301_001E': 'Total Workers 16+',
        'B08301_010E': 'Public Transportation to Work',
        'B08301_021E': 'Worked from Home',
        'B08303_001E': 'Travel Time to Work Total',
        'B15003_022E': "Bachelor's Degree",
        'B15003_023E': "Master's Degree",
        'B15003_024E': 'Professional Degree',
        'B15003_025E': 'Doctorate Degree'
    }

    params = {
        'get': ','.join(variables.keys()),
        'for': 'zip code tabulation area:21076',
        'key': api_key
    }

    print(f"Requesting ACS {year} data for {len(variables)} variables...")

    try:
        response = requests.get(base_url, params=params, timeout=int(os.getenv('API_TIMEOUT', '30')))
        response.raise_for_status()
        data = response.json()

        if not data or len(data) < 2:
            print("ERROR: No data returned from Census ACS API")
            return None

        headers = data[0]
        values = data[1]

        results = {}
        for i, header in enumerate(headers):
            if header in variables and i < len(values):
                raw_value = values[i]
                try:
                    if raw_value in ['-666666666', '-888888888', '-999999999', None]:
                        converted_value = None
                    else:
                        converted_value = int(raw_value)
                except (ValueError, TypeError):
                    converted_value = raw_value

                results[header] = {
                    'description': variables[header],
                    'raw_value': raw_value,
                    'value': converted_value
                }

        # Provenance and raw caching
        raw_dir = os.path.join('data', 'raw', 'census')
        saved_path = _save_raw(data, raw_dir, f'acs5_{year}_zcta21076')
        # Don't save API key in provenance
        provenance = {
            'endpoint': base_url,
            'year': year,
            'variables': list(variables.keys()),
            'geography': 'zip code tabulation area:21076',
            'retrieved_at': datetime.utcnow().isoformat() + 'Z',
            'raw_saved_to': saved_path
        }

        print(f"Successfully collected ACS data for {len(results)} variables")
        return {'data': results, 'provenance': provenance}

    except Exception as e:
        print(f"ERROR collecting ACS data: {e}")
        return None


def get_census_decennial_2020():
    """Get 2020 Decennial PL population for ZCTA 21076 for growth comparisons."""
    api_key = os.getenv('CENSUS_API_KEY')
    if not api_key:
        print("ERROR: Need CENSUS_API_KEY in .env file")
        return None

    base_url = 'https://api.census.gov/data/2020/dec/pl'
    variables = {
        'P1_001N': 'Total Population (Decennial 2020)'
    }
    params = {
        'get': ','.join(variables.keys()),
        'for': 'zip code tabulation area:21076',
        'key': api_key
    }

    print("Requesting 2020 Decennial PL population for ZCTA 21076...")
    try:
        response = requests.get(base_url, params=params, timeout=int(os.getenv('API_TIMEOUT', '30')))
        response.raise_for_status()
        data = response.json()
        if not data or len(data) < 2:
            print("ERROR: No data returned from Decennial API")
            return None
        headers = data[0]
        values = data[1]
        results = {}
        for i, header in enumerate(headers):
            if header in variables and i < len(values):
                try:
                    results[header] = {
                        'description': variables[header],
                        'raw_value': values[i],
                        'value': int(values[i])
                    }
                except (ValueError, TypeError):
                    results[header] = {
                        'description': variables[header],
                        'raw_value': values[i],
                        'value': None
                    }
        raw_dir = os.path.join('data', 'raw', 'census')
        saved_path = _save_raw(data, raw_dir, 'decennial_2020_pl_zcta21076')
        provenance = {
            'endpoint': base_url,
            'year': 2020,
            'variables': list(variables.keys()),
            'geography': 'zip code tabulation area:21076',
            'retrieved_at': datetime.utcnow().isoformat() + 'Z',
            'raw_saved_to': saved_path
        }
        print("Successfully collected Decennial 2020 population")
        return {'data': results, 'provenance': provenance}
    except Exception as e:
        print(f"ERROR collecting Decennial data: {e}")
        return None

def get_maryland_housing_data():
    """Placeholder for Maryland housing development data ingestion.

    Per project guardrails, do not hardcode state housing counts. Integrate an
    ingestion script from Maryland Open Data or MDP publications and persist
    raw+processed artifacts under data/raw and data/processed before using.
    """
    print("INFO: Maryland housing development data not yet integrated; skipping.")
    return None

def calculate_key_metrics(acs, decennial, housing_data):
    """Calculate the metrics that actually matter"""
    if not acs:
        return None

    metrics = {}

    # Population and growth
    acs_data = acs['data'] if isinstance(acs, dict) and 'data' in acs else acs
    total_pop = acs_data.get('B01003_001E', {}).get('value')
    if total_pop:
        metrics['population_2023'] = total_pop
    if decennial and isinstance(decennial, dict):
        pop2020 = decennial['data'].get('P1_001N', {}).get('value')
        if pop2020 and total_pop:
            metrics['population_2020'] = pop2020
            metrics['growth_rate'] = ((total_pop - pop2020) / pop2020) * 100

    # Housing crisis metrics
    total_housing = acs_data.get('B25001_001E', {}).get('value')
    occupied_owner = acs_data.get('B25003_002E', {}).get('value')
    occupied_renter = acs_data.get('B25003_003E', {}).get('value')

    if all([total_housing, occupied_owner, occupied_renter]):
        occupied_total = occupied_owner + occupied_renter
        vacancy_rate = ((total_housing - occupied_total) / total_housing) * 100
        metrics['vacancy_rate'] = vacancy_rate
        metrics['total_housing_units'] = total_housing
        metrics['occupied_units'] = occupied_total

    # Income and affordability
    median_income = acs_data.get('B19013_001E', {}).get('value')
    median_home_value = acs_data.get('B25077_001E', {}).get('value')
    median_gross_rent = acs_data.get('B25064_001E', {}).get('value')

    if median_income and median_home_value:
        price_to_income_ratio = median_home_value / median_income
        metrics['median_income'] = median_income
        metrics['median_home_value'] = median_home_value
        metrics['price_to_income_ratio'] = price_to_income_ratio
        metrics['affordable_home_price'] = median_income * 3  # Conventional heuristic (documented)
    if median_gross_rent:
        metrics['median_gross_rent'] = median_gross_rent

    # Transportation patterns
    total_workers = acs_data.get('B08301_001E', {}).get('value')
    public_transit = acs_data.get('B08301_010E', {}).get('value')
    work_from_home = acs_data.get('B08301_021E', {}).get('value')

    if total_workers and public_transit is not None and work_from_home is not None:
        metrics['total_workers'] = total_workers
        metrics['public_transit_rate'] = (public_transit / total_workers) * 100
        metrics['work_from_home_rate'] = (work_from_home / total_workers) * 100

    # Education levels (degree attainment)
    bachelor = acs_data.get('B15003_022E', {}).get('value', 0) or 0
    master = acs_data.get('B15003_023E', {}).get('value', 0) or 0
    professional = acs_data.get('B15003_024E', {}).get('value', 0) or 0
    doctorate = acs_data.get('B15003_025E', {}).get('value', 0) or 0

    if total_pop:
        college_plus_rate = ((bachelor + master + professional + doctorate) / total_pop) * 100
        metrics['college_plus_rate'] = college_plus_rate

    # Housing development trend (deferred until state data ingestion is wired)
    if housing_data:
        metrics['housing_development'] = housing_data

    return metrics

def save_results(acs, decennial, housing_data, metrics):
    """Save all data with timestamp"""
    timestamp = datetime.now().isoformat()

    results = {
        'collection_timestamp': timestamp,
        'geographic_area': 'ZIP 21076 (Hanover, MD)',
        'data_sources': {
            'census_acs5': 'ACS 5-Year Estimates 2023',
            'census_decennial_2020_pl': 'Decennial 2020 Public Law Redistricting Data',
            'housing': 'Maryland Department of Planning (pending integration)'
        },
        'raw_census_acs5': acs,
        'raw_census_decennial': decennial,
        'housing_development_data': housing_data,
        'calculated_metrics': metrics
    }

    # Create data directory
    os.makedirs('data', exist_ok=True)

    # Save detailed results
    with open('data/hanover_real_data.json', 'w') as f:
        json.dump(results, f, indent=2)

    # Create summary CSV for easy analysis
    if metrics:
        df = pd.DataFrame([metrics])
        df.to_csv('data/hanover_metrics.csv', index=False)

    print(f"Data saved to data/hanover_real_data.json and data/hanover_metrics.csv")
    return results

def main():
    """Collect real data for Hanover analysis"""
    print("HANOVER DATA COLLECTION - Real Census Data")
    print("=" * 50)

    # Collect Census data
    print("\n1. Collecting Census ACS data...")
    acs = get_census_acs5(year=int(os.getenv('DEFAULT_ACS_YEAR', '2023')))

    print("\n2. Collecting Decennial 2020 population...")
    decennial = get_census_decennial_2020()

    # Get housing development data (deferred)
    print("\n3. (Deferred) Getting Maryland housing data...")
    housing_data = get_maryland_housing_data()

    # Calculate key metrics
    print("\n4. Calculating key metrics...")
    metrics = calculate_key_metrics(acs, decennial, housing_data)

    # Save results
    print("\n5. Saving results...")
    results = save_results(acs, decennial, housing_data, metrics)

    # Print summary
    print("\n" + "=" * 50)
    print("DATA COLLECTION COMPLETE")
    print("=" * 50)

    if metrics:
        def _fmt(v, fmt='{:,}'):
            try:
                return fmt.format(v)
            except Exception:
                return 'N/A'

        print(f"Population (2023): {_fmt(metrics.get('population_2023'))}")
        if 'growth_rate' in metrics:
            print(f"Growth since 2020: {metrics.get('growth_rate'):.1f}%")
        print(f"Median Income: USD {_fmt(metrics.get('median_income'))}")
        if 'median_home_value' in metrics:
            print(f"Median Home Value: USD {_fmt(metrics.get('median_home_value'))}")
        if 'median_gross_rent' in metrics:
            print(f"Median Gross Rent: USD {_fmt(metrics.get('median_gross_rent'))}")
        if 'price_to_income_ratio' in metrics:
            print(f"Price-to-Income Ratio: {metrics.get('price_to_income_ratio'):.1f}")
        if 'vacancy_rate' in metrics:
            print(f"Vacancy Rate: {metrics.get('vacancy_rate'):.1f}%")
        if 'public_transit_rate' in metrics:
            print(f"Public Transit Rate: {metrics.get('public_transit_rate'):.1f}%")
        if 'work_from_home_rate' in metrics:
            print(f"Work from Home Rate: {metrics.get('work_from_home_rate'):.1f}%")
        if 'college_plus_rate' in metrics:
            print(f"College+ Rate: {metrics.get('college_plus_rate'):.1f}%")

    print(f"\nNext step: Create visualizations from data/hanover_real_data.json")

    return results

if __name__ == "__main__":
    main()