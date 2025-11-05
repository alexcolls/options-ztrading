# 📈 Options ZTrading

A terminal-based tool for fetching options data from Polygon.io API with concurrent processing support.

## ⚠️ FINANCIAL WARNINGS AND DISCLAIMERS

> IMPORTANT: READ BEFORE USE

### CRITICAL RISK NOTICE

1. EDUCATIONAL PURPOSES ONLY: This software is provided for educational and informational purposes only. It is NOT investment advice.
2. OPTIONS TRADING RISKS:
   - Options trading involves SUBSTANTIAL RISK of loss
   - You can lose MORE than your initial investment
   - Options can expire worthless, resulting in TOTAL LOSS of premium paid
   - Complex strategies can lead to UNLIMITED LOSSES
3. NO GUARANTEE OF PROFITS:
   - Past performance does NOT indicate future results
   - Backtested or hypothetical results are NOT indicative of future performance
   - Market conditions change and strategies that worked before may fail
4. YOUR RESPONSIBILITY:
   - You are SOLELY RESPONSIBLE for your trading decisions
   - Consult with qualified financial advisors before trading
   - Understand all fees, commissions, and tax implications
   - Review and comply with all regulatory requirements in your jurisdiction
5. DATA LIMITATIONS:
   - Data from Polygon.io may have delays or inaccuracies
   - Always verify data with your broker before trading
   - Ensure compliance with Polygon.io's terms of service and licensing
6. NO WARRANTY: This software is provided "AS IS" without any warranty, express or implied.

By using this software, you acknowledge that you understand and accept all risks involved in options trading.

---

## Features

- Fetch all active stock tickers from Polygon.io
- Fetch options snapshots with customizable parameters
- Concurrent API requests with basic rate-limit handling
- Environment-based configuration (.env files)
- Absolute path support for outputs
- CSV export for data analysis

## Prerequisites

- Python 3.10+
- Poetry (dependency and environment management)
- Polygon.io API key

## Installation

1) Clone the repository

```bash
git clone <repo-url>
cd options-ztrading
```

2) Install Poetry (if needed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3) Install dependencies

```bash
poetry install
```

4) Configure environment

```bash
cp .env.sample .env
# Edit .env and set POLYGON_API_KEY
```

## Configuration (.env)

```env
POLYGON_API_KEY=your_actual_api_key_here
OUTPUT_DIR=/absolute/path/to/data
DEFAULT_CONTRACT=put
DEFAULT_EXPIRATION=2024-01-19
DEFAULT_LIMIT=250
MAX_WORKERS=8
API_TIMEOUT=30
API_RETRY_COUNT=3
API_RETRY_DELAY=1
```

## Usage

Activate the environment (optional) or prefix commands with `poetry run`.

```bash
poetry shell
options --help
```

### Verify setup

```bash
options verify
```

### Fetch tickers

```bash
options fetch-tickers
# Custom output
options fetch-tickers --out /path/to/tickers.csv
# Include inactive tickers
options fetch-tickers --no-active-only
```

### Fetch options snapshots

```bash
# Use defaults from .env
options fetch-options

# Specify parameters
options fetch-options \
  --expiration 2024-02-16 \
  --contract put \
  --limit 100

# Fetch both calls and puts
options fetch-options --contract both

# Use a custom tickers list
options fetch-options --tickers /path/to/custom_tickers.csv

# Adjust concurrency
options fetch-options --max-workers 4
```

## Output format

Tickers CSV (one ticker per row):

```
ticker
AAPL
MSFT
...
```

Options CSV columns include: ticker, contract_type, strike_price, expiration_date, bid, ask, last_price, volume, open_interest, implied_volatility, fetch_timestamp, etc. Some fields depend on API availability.

## Notes

- Respect Polygon.io rate limits; adjust MAX_WORKERS and retry settings accordingly.
- Outputs are saved under `OUTPUT_DIR` (absolute path recommended).
- This tool is for data collection and education only; do not use it to make trading decisions.
