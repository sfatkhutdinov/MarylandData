#!/usr/bin/env python3
"""
Real Data Collection for Hanover, MD (ZIP 21076)
Collects actual Census and government data for rigorous analysis
"""

import requests
import json
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_census_data():
    """Get real Census data for ZIP 21076"""
    api_key = os.getenv('CENSUS_API_KEY')
    if not api_key:
        print("ERROR: Need CENSUS_API_KEY in .env file")
        print("Get one at: https://api.census.gov/data/key_signup.html")
        return None

    base_url = 'https://api.census.gov/data/2023/acs/acs5'

    # Core variables we actually need for analysis
    variables = {
        'B01003_001E': 'Total Population',
        'B19013_001E': 'Median Household Income',
        'B25077_001E': 'Median Home Value',
        'B25001_001E': 'Total Housing Units',
        'B25003_002E': 'Owner Occupied Housing',
        'B25003_003E': 'Renter Occupied Housing',
        'B25004_001E': 'Vacancy Status Total',
        'B08301_001E': 'Total Workers 16+',
        'B08301_010E': 'Public Transportation to Work',
        'B08301_021E': 'Worked from Home',
        'B08303_001E': 'Travel Time to Work Total',
        'B15003_022E': 'Bachelor\'s Degree',
        'B15003_023E': 'Master\'s Degree',
        'B15003_024E': 'Professional Degree',
        'B15003_025E': 'Doctorate Degree'
    }

    params = {
        'get': ','.join(variables.keys()),
        'for': 'zip code tabulation area:21076',
        'key': api_key
    }

    print(f"Requesting data for {len(variables)} variables...")

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data or len(data) < 2:
            print("ERROR: No data returned from Census API")
            return None

        headers = data[0]
        values = data[1]

        results = {}
        for i, header in enumerate(headers):
            if header in variables and i < len(values):
                raw_value = values[i]
                # Convert to int if possible, handle Census error codes
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

        print(f"Successfully collected data for {len(results)} variables")
        return results

    except Exception as e:
        print(f"ERROR collecting Census data: {e}")
        return None

def get_maryland_housing_data():
    """Get recent Maryland housing development data"""
    # Using the OpenGov MCP data we found earlier
    housing_data = {
        'howard_county_2022': 571,
        'howard_county_2021': 1735,
        'anne_arundel_2022': 1825,
        'anne_arundel_2021': 1745,
        'source': 'Maryland Department of Planning',
        'dataset': 'Total New Housing Units Authorized For Construction'
    }
    return housing_data

def calculate_key_metrics(census_data, housing_data):
    """Calculate the metrics that actually matter"""
    if not census_data:
        return None

    metrics = {}

    # Population and growth
    total_pop = census_data.get('B01003_001E', {}).get('value')
    if total_pop:
        metrics['population_2023'] = total_pop
        # Using external estimates for growth calculation
        metrics['population_2020'] = 22299  # From 2020 Census
        metrics['growth_rate'] = ((total_pop - 22299) / 22299) * 100

    # Housing crisis metrics
    total_housing = census_data.get('B25001_001E', {}).get('value')
    occupied_owner = census_data.get('B25003_002E', {}).get('value')
    occupied_renter = census_data.get('B25003_003E', {}).get('value')

    if all([total_housing, occupied_owner, occupied_renter]):
        occupied_total = occupied_owner + occupied_renter
        vacancy_rate = ((total_housing - occupied_total) / total_housing) * 100
        metrics['vacancy_rate'] = vacancy_rate
        metrics['total_housing_units'] = total_housing
        metrics['occupied_units'] = occupied_total

    # Income and affordability
    median_income = census_data.get('B19013_001E', {}).get('value')
    median_home_value = census_data.get('B25077_001E', {}).get('value')

    if median_income and median_home_value:
        price_to_income_ratio = median_home_value / median_income
        metrics['median_income'] = median_income
        metrics['median_home_value'] = median_home_value
        metrics['price_to_income_ratio'] = price_to_income_ratio
        metrics['affordable_home_price'] = median_income * 3  # Conservative ratio

    # Transportation patterns
    total_workers = census_data.get('B08301_001E', {}).get('value')
    public_transit = census_data.get('B08301_010E', {}).get('value')
    work_from_home = census_data.get('B08301_021E', {}).get('value')

    if total_workers and public_transit is not None and work_from_home is not None:
        metrics['total_workers'] = total_workers
        metrics['public_transit_rate'] = (public_transit / total_workers) * 100
        metrics['work_from_home_rate'] = (work_from_home / total_workers) * 100

    # Education levels (STEM proxy)
    bachelor = census_data.get('B15003_022E', {}).get('value', 0) or 0
    master = census_data.get('B15003_023E', {}).get('value', 0) or 0
    professional = census_data.get('B15003_024E', {}).get('value', 0) or 0
    doctorate = census_data.get('B15003_025E', {}).get('value', 0) or 0

    if total_pop:
        college_plus_rate = ((bachelor + master + professional + doctorate) / total_pop) * 100
        metrics['college_plus_rate'] = college_plus_rate

    # Housing development trend
    if housing_data:
        howard_decline = ((housing_data['howard_county_2021'] - housing_data['howard_county_2022']) /
                         housing_data['howard_county_2021']) * 100
        metrics['howard_housing_decline_2022'] = howard_decline

    return metrics

def save_results(census_data, housing_data, metrics):
    """Save all data with timestamp"""
    timestamp = datetime.now().isoformat()

    results = {
        'collection_timestamp': timestamp,
        'geographic_area': 'ZIP 21076 (Hanover, MD)',
        'data_sources': {
            'census': 'ACS 5-Year Estimates 2023',
            'housing': 'Maryland Department of Planning'
        },
        'raw_census_data': census_data,
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
    census_data = get_census_data()

    # Get housing development data
    print("\n2. Getting Maryland housing data...")
    housing_data = get_maryland_housing_data()

    # Calculate key metrics
    print("\n3. Calculating key metrics...")
    metrics = calculate_key_metrics(census_data, housing_data)

    # Save results
    print("\n4. Saving results...")
    results = save_results(census_data, housing_data, metrics)

    # Print summary
    print("\n" + "=" * 50)
    print("DATA COLLECTION COMPLETE")
    print("=" * 50)

    if metrics:
        print(f"Population (2023): {metrics.get('population_2023', 'N/A'):,}")
        print(f"Growth since 2020: {metrics.get('growth_rate', 'N/A'):.1f}%")
        print(f"Median Income: ${metrics.get('median_income', 'N/A'):,}")
        print(f"Median Home Value: ${metrics.get('median_home_value', 'N/A'):,}")
        print(f"Price-to-Income Ratio: {metrics.get('price_to_income_ratio', 'N/A'):.1f}")
        print(f"Vacancy Rate: {metrics.get('vacancy_rate', 'N/A'):.1f}%")
        print(f"Public Transit Rate: {metrics.get('public_transit_rate', 'N/A'):.1f}%")
        print(f"Work from Home Rate: {metrics.get('work_from_home_rate', 'N/A'):.1f}%")
        print(f"College+ Rate: {metrics.get('college_plus_rate', 'N/A'):.1f}%")
        print(f"Howard County Housing Decline (2022): {metrics.get('howard_housing_decline_2022', 'N/A'):.1f}%")

    print(f"\nNext step: Create visualizations from data/hanover_real_data.json")

    return results

if __name__ == "__main__":
    main()