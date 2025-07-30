import httpx
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

"""
GLEIF Model Context Protocol (MCP) Server
========================================
This MCP server exposes a *tool* for each of the primary resources documented in
GLEIF's public REST API v1.0 – see the full list at
https://documenter.getpostman.com/view/7679680/SVYrrxuU?version=latest.

The goal is to make the GLEIF dataset easily accessible to large‑language‑model
agents via MCP by wrapping the most frequently‑used endpoints as individual
MCP **tools**.

Covered resources / tools
-------------------------
• LEI records
  • list_lei_records              GET /lei-records
  • get_lei_record                GET /lei-records/{lei}
  • search_lei_records            GET /lei-records?filter[…]
• Relationship helpers (fuzzy / auto completion)
  • fuzzy_completions             GET /fuzzycompletions
  • auto_completions              GET /autocompletions
• LEI issuers (Managing LOU)
  • list_lei_issuers              GET /lei-issuers
  • get_lei_issuer                GET /lei-issuers/{id}
• Reference data
  • list_countries                GET /countries
  • get_country                   GET /countries/{code}
  • list_entity_legal_forms       GET /entity-legal-forms
  • get_entity_legal_form         GET /entity-legal-forms/{id}
• Metadata
  • list_fields                   GET /fields
  • get_field_details             GET /fields/{id}

Each tool returns the raw JSON payload from the GLEIF API or a JSON structure
of the form {"error": "…"} when a problem occurs.
"""

GLEIF_API_BASE_URL = "https://api.gleif.org/api/v1"

# ---------------------------------------------------------------------------
# Helper – unified GET wrapper
# ---------------------------------------------------------------------------

def _request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Perform a GET request against the GLEIF API and return JSON (or error)."""
    url = f"{GLEIF_API_BASE_URL}{endpoint}"
    try:
        with httpx.Client(timeout=30) as client:
            response = client.get(url, params=params or {})
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text}"}
    except httpx.RequestError as exc:
        return {"error": f"Request error: {exc!s}"}


# ---------------------------------------------------------------------------
# MCP server & tools
# ---------------------------------------------------------------------------

server = FastMCP("GLEIF API Server")

# --- LEI records -----------------------------------------------------------

@server.tool()
def list_lei_records(page: int = 1, size: int = 25) -> Dict[str, Any]:
    """Return a paginated list of LEI records (Level‑1 data)."""
    params = {"page[number]": page, "page[size]": size}
    return _request("/lei-records", params)


@server.tool()
def get_lei_record(lei: str) -> Dict[str, Any]:
    """Retrieve a single LEI record by its 20‑character LEI code."""
    return _request(f"/lei-records/{lei}")


@server.tool()
def search_lei_records(filter_key: str, filter_value: str, page: int = 1, size: int = 25) -> Dict[str, Any]:
    """General‑purpose LEI search using any supported filter field.

    Example: search_lei_records("entity.legalName", "Citibank")
    See the documentation for allowed fields & operators.
    """
    params = {
        f"filter[{filter_key}]": filter_value,
        "page[number]": page,
        "page[size]": size,
    }
    return _request("/lei-records", params)


# --- Relationship helpers (fuzzy / auto completion) -----------------------

@server.tool()
def fuzzy_completions(field: str, query: str, page: int = 1, size: int = 15) -> Dict[str, Any]:
    """Approximate‑match search (e.g. suggest entities similar to *query*)."""
    params = {
        "field": field,
        "q": query,
        "page[number]": page,
        "page[size]": size,
    }
    return _request("/fuzzycompletions", params)


@server.tool()
def auto_completions(field: str, query: str, page: int = 1, size: int = 15) -> Dict[str, Any]:
    """Return suggested search terms based on *query*."""
    params = {
        "field": field,
        "q": query,
        "page[number]": page,
        "page[size]": size,
    }
    return _request("/autocompletions", params)


# --- LEI issuers -----------------------------------------------------------

@server.tool()
def list_lei_issuers(page: int = 1, size: int = 25) -> Dict[str, Any]:
    """Retrieve the list of accredited LEI Issuers (Managing LOUs)."""
    params = {"page[number]": page, "page[size]": size}
    return _request("/lei-issuers", params)


@server.tool()
def get_lei_issuer(issuer_id: str) -> Dict[str, Any]:
    """Get details about a single LEI issuer by its numeric ID."""
    return _request(f"/lei-issuers/{issuer_id}")


# --- Reference data --------------------------------------------------------

@server.tool()
def list_countries(page: int = 1, size: int = 250) -> Dict[str, Any]:
    """Return ISO‑3166 country codes recognised by the API."""
    params = {"page[number]": page, "page[size]": size}
    return _request("/countries", params)


@server.tool()
def get_country(code: str) -> Dict[str, Any]:
    """Country lookup (two‑letter code, e.g. 'US')."""
    return _request(f"/countries/{code}")


@server.tool()
def list_entity_legal_forms(page: int = 1, size: int = 250) -> Dict[str, Any]:
    """List Entity Legal Forms (ELF codes)."""
    params = {"page[number]": page, "page[size]": size}
    return _request("/entity-legal-forms", params)


@server.tool()
def get_entity_legal_form(form_id: str) -> Dict[str, Any]:
    """Retrieve details for a specific legal form by its ELF code."""
    return _request(f"/entity-legal-forms/{form_id}")


# --- Metadata --------------------------------------------------------------

@server.tool()
def list_fields(page: int = 1, size: int = 250) -> Dict[str, Any]:
    """Return the catalogue of data fields that can be filtered / sorted."""
    params = {"page[number]": page, "page[size]": size}
    return _request("/fields", params)


@server.tool()
def get_field_details(field_id: str) -> Dict[str, Any]:
    """Retrieve metadata for a specific field (ID from list_fields)."""
    return _request(f"/fields/{field_id}")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    server.run()
