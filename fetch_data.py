#!/usr/bin/env python3
"""
Fetch Taiwan stock data from FinMind API and build data.json
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


def get_date_range():
    """Return today and 3 years ago in YYYY-MM-DD format"""
    today = datetime.now()
    three_years_ago = today - timedelta(days=3*365)
    return today.strftime('%Y-%m-%d'), three_years_ago.strftime('%Y-%m-%d')


def fetch_stock_data(symbol, token=None):
    """Fetch stock price data for a symbol. Returns list of records or None on failure."""
    today, start_date = get_date_range()

    url = f"https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockPrice&data_id={symbol}&start_date={start_date}"
    if token:
        url += f"&token={token}"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 200 and data.get('msg') == 'success':
                    return data.get('data', [])
            print(f"Warning: Symbol {symbol} attempt {attempt + 1}/3 returned status {response.status_code}", file=sys.stderr)
        except requests.exceptions.RequestException as e:
            print(f"Warning: Symbol {symbol} attempt {attempt + 1}/3 failed: {e}", file=sys.stderr)

        if attempt < 2:
            time.sleep(5)

    print(f"Warning: Failed to fetch data for symbol {symbol} after 3 retries", file=sys.stderr)
    return None


def build_data_json():
    """Main function to fetch all symbols and build data.json"""
    symbols = ["TAIEX", "2330", "0050", "0056", "006208", "00646"]
    token = os.environ.get('FINMIND_TOKEN')

    output = {
        "_updated": datetime.utcnow().isoformat() + "Z",
        "stocks": {}
    }

    for symbol in symbols:
        print(f"Fetching {symbol}...")
        records = fetch_stock_data(symbol, token)

        if records is None:
            print(f"Skipping {symbol} due to fetch failure", file=sys.stderr)
        else:
            # Sort by date (ascending) and extract dates and closes
            records.sort(key=lambda x: x.get('date', ''))

            dates = []
            closes = []

            for record in records:
                close = record.get('close')
                # Skip rows with null or 0 close
                if close is None or close == 0:
                    continue

                date_str = record.get('date')
                if date_str:
                    dates.append(date_str)
                    # Round close to 2 decimals
                    closes.append(round(float(close), 2))

            if dates and closes:
                output["stocks"][symbol] = {
                    "dates": dates,
                    "close": closes
                }
                print(f"  -> {len(dates)} records for {symbol}")

        # Be polite to the API
        time.sleep(1)

    # Write data.json
    script_dir = Path(__file__).parent
    output_path = script_dir / "data.json"

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✓ Data written to {output_path}")


if __name__ == "__main__":
    build_data_json()
