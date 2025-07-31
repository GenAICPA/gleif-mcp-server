"""Internal helpers for the GLEIF API client."""

import httpx
from typing import Dict, Any, Optional

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
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text}"}
    except httpx.RequestError as exc:
        return {"error": f"Request error: {exc!s}"}

def _request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make a request to the GLEIF API.
    
    Args:
        endpoint: API endpoint path
        params: Optional query parameters
        
    Returns:
        Parsed JSON response or error dict
    """
    url = _build_url(GLEIF_BASE_URL, endpoint)
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, params=params or {})
            return _handle_response(response)
    except Exception as exc:
        return {"error": f"Request failed: {exc!s}"}