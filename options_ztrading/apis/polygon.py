"""Polygon.io API client."""
import time
from typing import Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config import (
    POLYGON_API_KEY,
    API_TIMEOUT,
    API_RETRY_COUNT,
    API_RETRY_DELAY,
)


class PolygonClient:
    """Client for Polygon.io API with retry logic."""

    BASE_URL = "https://api.polygon.io"

    def __init__(self):
        self.session = self._create_session()
        self.api_key = POLYGON_API_KEY

    def _create_session(self) -> requests.Session:
        """Create a session with retry strategy."""
        session = requests.Session()
        retry_strategy = Retry(
            total=API_RETRY_COUNT,
            backoff_factor=API_RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request to Polygon API."""
        if params is None:
            params = {}
        params["apiKey"] = self.api_key

        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=API_TIMEOUT)

            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", API_RETRY_DELAY))
                time.sleep(retry_after)
                return self.get(endpoint, params)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")
