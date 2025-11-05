"""Service for fetching stock tickers."""
from pathlib import Path
from typing import List, Optional
import pandas as pd

from ..apis.polygon import PolygonClient
from ..config import DATA_DIR


def fetch_all_tickers(
    limit: int = 1000,
    market: str = "stocks",
    active: bool = True,
) -> List[str]:
    """
    Fetch all stock tickers from Polygon.io.

    Args:
        limit: Maximum number of tickers per request
        market: Market type (stocks, crypto, fx)
        active: Only fetch active tickers

    Returns:
        List of ticker symbols
    """
    client = PolygonClient()
    tickers: List[str] = []
    next_url: Optional[str] = None

    params = {
        "limit": limit,
        "market": market,
        "active": active,
    }

    while True:
        if next_url:
            # Use pagination URL
            resp = client.session.get(next_url, params={"apiKey": client.api_key})
            resp.raise_for_status()
            data = resp.json()
        else:
            data = client.get("/v3/reference/tickers", params)

        if "results" in data:
            tickers.extend([t["ticker"] for t in data["results"]])

        # Check for pagination
        if data.get("next_url"):
            next_url = data["next_url"]
        else:
            break

    return tickers


def save_tickers_to_csv(tickers: List[str], output_path: Optional[Path] = None) -> Path:
    """
    Save tickers to CSV file.

    Args:
        tickers: List of ticker symbols
        output_path: Optional custom output path

    Returns:
        Path to the saved CSV file
    """
    if output_path is None:
        output_path = DATA_DIR / "tickers.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write as columnar CSV (one ticker per row)
    df = pd.DataFrame({"ticker": tickers})
    df.to_csv(output_path, index=False)

    return output_path


def load_tickers_from_csv(file_path: Optional[Path] = None) -> List[str]:
    """
    Load tickers from CSV file.

    Args:
        file_path: Path to CSV file (default: DATA_DIR/tickers.csv)

    Returns:
        List of ticker symbols
    """
    if file_path is None:
        file_path = DATA_DIR / "tickers.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Tickers file not found: {file_path}")

    df = pd.read_csv(file_path)
    return df["ticker"].tolist()
