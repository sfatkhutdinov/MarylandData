# 🔑 API Keys & Setup Guide

**Essential setup for MarylandData project data collection**

## 📋 Quick Setup Checklist

- [ ] Copy `.env.example` to `.env`
- [ ] Get Census Bureau API key (required)
- [ ] Configure environment variables
- [ ] Test API connectivity
- [ ] Optional: Get BLS API key for enhanced features

---

## 🏛️ Census Bureau API Key (REQUIRED)

### Why This is Essential
The Census Bureau API is our primary source for ZIP 21076 demographic data. **The project cannot collect real data without this key.**

### Getting Your Key
1. **Visit**: https://api.census.gov/data/key_signup.html
2. **Fill out**: Basic information (name, email, organization)
3. **Purpose**: "Academic research on community improvement analysis"
4. **Receive**: API key via email (usually instant)

### Rate Limits
- **500 requests per day** per IP address
- **No cost** - completely free
- **No credit card** required

### Adding to Project
```bash
# Copy the template
cp .env.example .env

# Edit .env and add your key
CENSUS_API_KEY=your_actual_key_here
```

---

## 📊 Bureau of Labor Statistics API Key (OPTIONAL)

### Why This Helps
BLS data provides employment statistics for our economic analysis. The API key increases rate limits from 25 to 500 requests per day.

### Getting Your Key
1. **Visit**: https://data.bls.gov/registrationEngine/
2. **Register**: Email and basic information
3. **Verify**: Email confirmation
4. **Use**: Key in API requests

### Adding to Project
```bash
# Add to your .env file
BLS_API_KEY=your_bls_key_here
```

---

## 🧪 Testing Your Setup

### Basic Connectivity Test
```python
# Run from project root
python scripts/hanover_data_collector.py
```

Expected output:
```
🚀 Initializing Hanover Data Collector...
📡 Testing API connectivity...
✅ census_api: Connected
📊 Testing demographic data collection...
✅ Demographics collected successfully!
   Population: 28089
   Data Quality Score: 95/100
```

### Manual API Test
```python
from scripts.hanover_data_collector import HanoverDataCollector

collector = HanoverDataCollector()
connectivity = collector.test_api_connectivity()
print(connectivity)
```

---

## 🔒 Security Best Practices

### Environment File Security
```bash
# NEVER commit .env to git (already in .gitignore)
git status  # Should not show .env file

# Keep backup of your keys securely
# Consider using a password manager
```

### Key Rotation
- **If exposed**: Request new keys immediately
- **Regular rotation**: Good practice every 6-12 months
- **Monitor usage**: Census provides usage statistics

---

## 🚨 Troubleshooting

### "Census API key not found" Warning
```python
# Check your .env file exists and has the right variable name
ls -la .env
cat .env | grep CENSUS_API_KEY
```

### "API request failed" Errors
1. **Check internet connection**
2. **Verify API key is correct** (no extra spaces)
3. **Check rate limits** (500/day for Census)
4. **Try different endpoint** (API may have temporary issues)

### Rate Limit Exceeded
```
HTTP 429 Too Many Requests
```
**Solution**: Wait until next day or optimize requests

---

## 🎯 Data Collection Strategy

### Daily Request Budget
- **Census API**: 500 requests/day
- **ZIP 21076 demographics**: ~20 requests
- **Comparative analysis**: ~80 requests (ZIP + County + State + National)
- **Monthly data collection**: Well within limits

### Optimization
```python
# Use comparative data collection for efficiency
collector = HanoverDataCollector()
comparative_data = collector.get_comparative_data(['B01003_001E', 'B19013_001E'])
# This gets all geographic levels in one efficient batch
```

---

## ✅ Verification Commands

### Test Environment Loading
```python
from dotenv import load_dotenv
import os

load_dotenv()
print(f"Census key loaded: {bool(os.getenv('CENSUS_API_KEY'))}")
print(f"BLS key loaded: {bool(os.getenv('BLS_API_KEY'))}")
```

### Test Data Collection
```python
from scripts.hanover_data_collector import HanoverDataCollector

collector = HanoverDataCollector()
demographics = collector.get_acs_demographics()
print(f"Success: {demographics.success}")
print(f"Population: {demographics.data['estimates'].get('B01003_001E', 'N/A')}")
```

---

## 📞 Support Resources

- **Census API Documentation**: https://www.census.gov/data/developers/data-sets/acs-5year.html
- **Variable Reference**: https://api.census.gov/data/2023/acs/acs5/variables.json
- **BLS API Documentation**: https://www.bls.gov/developers/api_signature_v2.htm
- **Project Issues**: See GitHub repository issues