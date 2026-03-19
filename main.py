from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import PlainTextResponse
from fastapi.security.api_key import APIKeyHeader
import requests

# ---------------------------
# CONFIGURATION
# ---------------------------

API_KEY = "mysecret123"  # FastAPI API Key (you use this in Swagger/curl)
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # 🔴 Replace with your Gemini key

VALID_SECTORS = [
    "technology",
    "finance",
    "healthcare",
    "energy",
    "pharmaceuticals",
    "agriculture"
]

app = FastAPI(title="Market Analysis API", version="1.0")

# ---------------------------
# AUTHENTICATION
# ---------------------------

api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)

async def authenticate(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------

def validate_sector(sector: str):
    if sector.lower() not in VALID_SECTORS:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid sector. Choose from {VALID_SECTORS}"
        )
    return sector.lower()

def fetch_market_data(sector: str):
    """
    Mock data (ensures API always works)
    """
    mock_data = {
        "technology": {"index": 14500.23, "trend": "positive"},
        "finance": {"index": 10230.45, "trend": "neutral"},
        "healthcare": {"index": 8700.12, "trend": "positive"},
        "energy": {"index": 5400.67, "trend": "negative"},
        "pharmaceuticals": {"index": 7200.34, "trend": "positive"},
        "agriculture": {"index": 6500.89, "trend": "neutral"}
    }
    return {"sector": sector.title(), **mock_data.get(sector, {"index": 1000, "trend": "neutral"})}

def generate_gemini_report(market_data: dict):
    """
    Try Gemini → If fails → return professional fallback report
    """

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"""
    Create a professional markdown market analysis report for the {market_data['sector']} sector.

    Include:
    - Summary
    - Trade opportunities
    - Key statistics
    - Market trend

    Data:
    {market_data}
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except:
        # ✅ Professional fallback report
        return f"""# Market Analysis Report: {market_data['sector']}

## 📊 Summary
The {market_data['sector']} sector is currently showing a **{market_data['trend']} trend**. Market conditions indicate steady movement with potential growth opportunities.

## 📈 Key Statistics
- **Sector Index**: {market_data['index']}
- **Market Trend**: {market_data['trend'].capitalize()}
- **Volatility**: Medium
- **Growth Outlook**: Stable to Positive

## 💡 Trade Opportunities
- Identify high-performing stocks in the {market_data['sector']} sector
- Monitor short-term fluctuations for trading opportunities
- Consider long-term investments based on trend stability

## ⚠️ Risk Factors
- Market volatility due to global conditions
- Sector-specific regulations
- Demand-supply changes

## 🧾 Conclusion
The {market_data['sector']} sector shows a **{market_data['trend']} outlook**, offering balanced opportunities for investors and traders.

---
*Note: This is a fallback report (Gemini API unavailable).*
"""

# ---------------------------
# MAIN ENDPOINT
# ---------------------------

@app.get("/analyze/{sector}", response_class=PlainTextResponse)
async def analyze(sector: str, request: Request, auth: bool = Depends(authenticate)):
    """
    Main endpoint:
    - Input: sector name
    - Output: markdown market analysis report
    """
    sector = validate_sector(sector)
    market_data = fetch_market_data(sector)
    report = generate_gemini_report(market_data)
    return report

# ---------------------------
# ROOT
# ---------------------------

@app.get("/")
async def root():
    return {"message": "Market Analysis API is running. Go to /docs"}