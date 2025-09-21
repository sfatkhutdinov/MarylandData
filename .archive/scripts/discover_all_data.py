#!/usr/bin/env python3
"""
True Raw Data Discovery - no hardcoded assumptions

Discovers what data is actually available for ZIP 21076 by trying
everything and seeing what comes back.
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def discover_all_available_data():
    """Find what data actually exists for ZIP 21076 by testing everything."""
    
    api_key = os.getenv('CENSUS_API_KEY')
    if not api_key:
        print("Need CENSUS_API_KEY in .env")
        return
        
    base_url = 'https://api.census.gov/data/2023/acs/acs5'
    
    print("Getting all available variables...")
    
    # Get ALL variables
    try:
        response = requests.get(f"{base_url}/variables.json")
        response.raise_for_status()
        all_variables = response.json()['variables']
        
        # Filter to estimate variables only
        estimate_vars = [var for var in all_variables.keys() 
                        if var.endswith('E') and var not in ['for', 'in', 'ucgid']]
        
        print(f"Found {len(estimate_vars)} estimate variables to test")
        
    except Exception as e:
        print(f"Error getting variables: {e}")
        return
    
    # Test variables in batches to see what actually has data for ZIP 21076
    print("Testing which variables have data for ZIP 21076...")
    
    batch_size = 50
    available_data = {}
    
    for i in range(0, len(estimate_vars), batch_size):
        batch = estimate_vars[i:i+batch_size]
        batch_num = i//batch_size + 1
        
        print(f"Testing batch {batch_num}/{(len(estimate_vars)//batch_size)+1}: {len(batch)} variables")
        
        params = {
            'get': ','.join(batch),
            'for': 'zip code tabulation area:21076',
            'key': api_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) >= 2:
                headers = data[0]
                values = data[1]
                
                for j, header in enumerate(headers):
                    if header != 'zip code tabulation area' and j < len(values):
                        value = values[j]
                        # Save ALL values - let the user decide what's valid
                        available_data[header] = {
                            'value': value,
                            'definition': all_variables.get(header, {}).get('label', 'No definition')
                        }
                            
                print(f"  Found {len([h for h in headers if h in available_data])} variables with data")
                
        except Exception as e:
            print(f"  Batch {batch_num} failed: {e}")
            continue
    
    print(f"\n✅ Discovery complete!")
    print(f"Variables with actual data for ZIP 21076: {len(available_data)}")
    
    # Save the discovered data
    os.makedirs('data/raw', exist_ok=True)
    
    with open('data/raw/zip_21076_discovered_data.json', 'w') as f:
        json.dump({
            'metadata': {
                'zip_code': '21076',
                'total_variables_tested': len(estimate_vars),
                'variables_with_data': len(available_data),
                'discovery_method': 'Tested all available variables',
                'api_source': base_url
            },
            'data': available_data
        }, f, indent=2)
    
    # Create human-readable summary
    print("\n📋 Sample of available data:")
    for i, (var_code, var_data) in enumerate(list(available_data.items())[:10]):
        print(f"{var_code}: {var_data['value']}")
        print(f"  {var_data['definition']}")
        
    if len(available_data) > 10:
        print(f"... and {len(available_data) - 10} more variables")
        
    print(f"\n📄 Complete data saved to: data/raw/zip_21076_discovered_data.json")
    
    return available_data

if __name__ == "__main__":
    discover_all_available_data()