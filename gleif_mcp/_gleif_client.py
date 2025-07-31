"""Internal helpers for the GLEIF API client."""

import httpx
from typing import Dict, Any

GLEIF_BASE_URL = "https://api.gleif.org/api/v1"

def _build_url(base_url: str, endpoint: str) -> str:
    """Construct a full URL from a base and an endpoint."""
    return f"{base_url}{endpoint}"

def _handle_response(response: httpx.Response) -> Dict[str, Any]:
    """Handle HTTP responses and return JSON or raise an error."""
    try:
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        raise Exception(f"HTTP {exc.response.status_code}: {exc.response.text}") from exc
    except httpx.RequestError as exc:
        raise Exception(f"Request error: {exc!s}") from exc
