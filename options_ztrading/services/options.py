"""Service for fetching options data."""
import concurrent.futures
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Literal
import pandas as pd
from tqdm import tqdm

from ..apis.polygon import PolygonClient
from ..config import DATA_DIR, MAX_WORKERS


ContractType = Literal["call", "put", "both"]


def fetch_option_snapshot(
    ticker: str,
    expiration: str,
    contract_type: str = "put",
    limit: int = 250,
) -> Optional[pd.DataFrame]:
    """
    Fetch options snapshot for a single ticker.

    Args:
        ticker: Stock ticker symbol
        expiration: Expiration date (YYYY-MM-DD)
        contract_type: Type of contract (call/put)
        limit: Maximum number of contracts to fetch

    Returns:
        DataFrame with options data or None if error
    """
    client = PolygonClient()

    try:
        # Endpoint
        endpoint = f"/v3/snapshot/options/{ticker}"

        params = {
            "contract_type": contract_type,
            "expiration_date": expiration,
            "limit": limit,
            "sort": "strike_price",
            "order": "asc",
        }

        data = client.get(endpoint, params)

        if "results" not in data or not data["results"]:
            return None

        # Flatten and normalize selected fields if necessary
        df = pd.json_normalize(data["results"])  # handles nested structures

        # Add metadata columns
        df["ticker"] = ticker
        df["fetch_timestamp"] = datetime.now().isoformat()

        return df

    except Exception as e:
        print(f"Error fetching options for {ticker}: {e}")
        return None


def fetch_options_snapshot(
    tickers: List[str],
    expiration: str,
    contract_type: ContractType = "put",
    limit: int = 250,
    max_workers: Optional[int] = None,
    show_progress: bool = True,
) -> pd.DataFrame:
    """
    Fetch options snapshots for multiple tickers concurrently.

    Args:
        tickers: List of stock ticker symbols
        expiration: Expiration date (YYYY-MM-DD)
        contract_type: Type of contract (call/put/both)
        limit: Maximum number of contracts per ticker
        max_workers: Maximum number of concurrent workers
        show_progress: Show progress bar

    Returns:
        Combined DataFrame with all options data
    """
    if max_workers is None:
        max_workers = MAX_WORKERS

    all_results = []

    if contract_type == "both":
        contract_types = ["call", "put"]
    else:
        contract_types = [contract_type]

    for ct in contract_types:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    fetch_option_snapshot, ticker, expiration, ct, limit
                ): ticker
                for ticker in tickers
            }

            iterator = concurrent.futures.as_completed(futures)
            if show_progress:
                iterator = tqdm(
                    iterator,
                    total=len(futures),
                    desc=f"Fetching {ct} options",
                )

            for future in iterator:
                result = future.result()
                if result is not None:
                    if contract_type == "both":
                        result["contract_type"] = ct
                    all_results.append(result)

    if all_results:
        return pd.concat(all_results, ignore_index=True)
    else:
        return pd.DataFrame()


def save_options_to_csv(
    df: pd.DataFrame,
    output_path: Optional[Path] = None,
    contract_type: str = "options",
    expiration: Optional[str] = None,
) -> Path:
    """
    Save options data to CSV file.

    Args:
        df: DataFrame with options data
        output_path: Optional custom output path
        contract_type: Contract type for filename
        expiration: Expiration date for filename

    Returns:
        Path to the saved CSV file
    """
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{contract_type}_options"
        if expiration:
            filename += f"_{expiration}"
        filename += f"_{timestamp}.csv"
        output_path = DATA_DIR / filename

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    return output_path
