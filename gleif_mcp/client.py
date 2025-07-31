"""GLEIF API Python Client.

This module provides a convenient Python client for accessing the GLEIF API
without needing to run the MCP server. It's useful for direct API access
in Python applications.

Example:
    >>> from gleif_mcp.client import GleifClient
    >>> client = GleifClient()
    >>> record = client.get_lei_record("529900T8BM49AURSDO55")
    >>> print(record['entity']['legalName'])
    
    >>> # Search for entities
    >>> results = client.search_lei_records("entity.legalName", "Apple")
    >>> for entity in results['data'][:5]:
    ...     print(f"{entity['lei']}: {entity['entity']['legalName']}")
"""

import asyncio
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

import httpx

from gleif_mcp._gleif_client import GLEIF_BASE_URL, _build_url, _handle_response


class GleifClient:
    """Synchronous client for the GLEIF API.
    
    This client provides a simple Python interface to all GLEIF API endpoints.
    It handles authentication, error handling, and response parsing automatically.
    
    Attributes:
        base_url: The base URL for the GLEIF API
        timeout: HTTP request timeout in seconds
        
    Example:
        >>> client = GleifClient(timeout=30.0)
        >>> record = client.get_lei_record("529900T8BM49AURSDO55")
        >>> print(record['entity']['legalName'])
    """
    
    def __init__(
        self,
        base_url: str = GLEIF_BASE_URL,
        timeout: float = 30.0,
        user_agent: str = "gleif-mcp-client/0.1.0",
    ):
        """Initialize the GLEIF client.
        
        Args:
            base_url: Base URL for the GLEIF API
            timeout: Request timeout in seconds
            user_agent: User agent string for requests
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = {
            "User-Agent": user_agent,
            "Accept": "application/json",
        }

    def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a synchronous HTTP request to the GLEIF API.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            Parsed JSON response
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        url = _build_url(self.base_url, endpoint)
        
        with httpx.Client(timeout=self.timeout, headers=self.headers) as client:
            response = client.get(url, params=params or {})
            return _handle_response(response)

    # LEI Records
    def list_lei_records(self, page: int = 1, size: int = 25) -> Dict[str, Any]:
        """Retrieve a paginated list of LEI records.
        
        Args:
            page: Page number (1-based)
            size: Number of records per page (max 200)
            
        Returns:
            Dictionary containing LEI records and pagination metadata
        """
        return self._request("/lei-records", {"page": page, "size": size})

    def get_lei_record(self, lei: str) -> Dict[str, Any]:
        """Retrieve a single LEI record by its 20-character LEI code.
        
        Args:
            lei: The 20-character LEI code
            
        Returns:
            Dictionary containing the LEI record data
            
        Raises:
            httpx.HTTPError: If the LEI is not found or invalid
        """
        return self._request(f"/lei-records/{quote(lei)}")

    def search_lei_records(
        self,
        filter_key: str,
        filter_value: str,
        page: int = 1,
        size: int = 25,
    ) -> Dict[str, Any]:
        """Search LEI records using field-based filtering.
        
        Args:
            filter_key: Field to filter on (e.g., "entity.legalName")
            filter_value: Value to match (supports wildcards with *)
            page: Page number (1-based)
            size: Number of records per page
            
        Returns:
            Dictionary containing matching LEI records
            
        Example:
            >>> client.search_lei_records("entity.legalName", "*Apple*")
            >>> client.search_lei_records("entity.jurisdiction", "US")
        """
        params = {
            f"filter[{filter_key}]": filter_value,
            "page": page,
            "size": size,
        }
        return self._request("/lei-records", params)

    def fuzzy_completions(
        self,
        field: str,
        query: str,
        page: int = 1,
        size: int = 15,
    ) -> Dict[str, Any]:
        """Get fuzzy matching suggestions for entity names.
        
        Args:
            field: Field to search in (e.g., "entity.legalName")
            query: Partial text to match
            page: Page number (1-based)
            size: Number of suggestions to return
            
        Returns:
            Dictionary containing fuzzy match suggestions
        """
        params = {
            "field": field,
            "q": query,
            "page": page,
            "size": size,
        }
        return self._request("/lei-records/fuzzy-completions", params)

    def auto_completions(
        self,
        field: str,
        query: str,
        page: int = 1,
        size: int = 15,
    ) -> Dict[str, Any]:
        """Get auto-completion suggestions for search terms.
        
        Args:
            field: Field to search in
            query: Partial text to complete
            page: Page number (1-based)
            size: Number of completions to return
            
        Returns:
            Dictionary containing auto-completion suggestions
        """
        params = {
            "field": field,
            "q": query,
            "page": page,
            "size": size,
        }
        return self._request("/lei-records/auto-completions", params)

    # LEI Issuers
    def list_lei_issuers(self, page: int = 1, size: int = 25) -> Dict[str, Any]:
        """Retrieve the list of accredited LEI Issuers (Managing LOUs).
        
        Args:
            page: Page number (1-based)
            size: Number of issuers per page
            
        Returns:
            Dictionary containing LEI issuer information
        """
        return self._request("/lei-issuers", {"page": page, "size": size})

    def get_lei_issuer(self, issuer_id: str) -> Dict[str, Any]:
        """Get details about a single LEI issuer by its numeric ID.
        
        Args:
            issuer_id: The issuer's numeric identifier
            
        Returns:
            Dictionary containing issuer details
        """
        return self._request(f"/lei-issuers/{quote(issuer_id)}")

    # Reference Data
    def list_countries(self, page: int = 1, size: int = 250) -> Dict[str, Any]:
        """Return ISO 3166 country codes recognized by the API.
        
        Args:
            page: Page number (1-based)
            size: Number of countries per page
            
        Returns:
            Dictionary containing country information
        """
        return self._request("/countries", {"page": page, "size": size})

    def get_country(self, code: str) -> Dict[str, Any]:
        """Country lookup by two-letter ISO code.
        
        Args:
            code: Two-letter country code (e.g., 'US', 'GB')
            
        Returns:
            Dictionary containing country details
        """
        return self._request(f"/countries/{quote(code.upper())}")

    def list_entity_legal_forms(self, page: int = 1, size: int = 250) -> Dict[str, Any]:
        """List Entity Legal Forms (ELF codes).
        
        Args:
            page: Page number (1-based)
            size: Number of legal forms per page
            
        Returns:
            Dictionary containing legal form information
        """
        return self._request("/entity-legal-forms", {"page": page, "size": size})

    def get_entity_legal_form(self, form_id: str) -> Dict[str, Any]:
        """Retrieve details for a specific legal form by its ELF code.
        
        Args:
            form_id: The Entity Legal Form code
            
        Returns:
            Dictionary containing legal form details
        """
        return self._request(f"/entity-legal-forms/{quote(form_id)}")

    # Metadata
    def list_fields(self, page: int = 1, size: int = 250) -> Dict[str, Any]:
        """Return the catalog of data fields that can be filtered/sorted.
        
        Args:
            page: Page number (1-based)
            size: Number of fields per page
            
        Returns:
            Dictionary containing field metadata
        """
        return self._request("/fields", {"page": page, "size": size})

    def get_field_details(self, field_id: str) -> Dict[str, Any]:
        """Retrieve metadata for a specific field.
        
        Args:
            field_id: The field identifier from list_fields()
            
        Returns:
            Dictionary containing field details
        """
        return self._request(f"/fields/{quote(field_id)}")

    # Convenience methods
    def search_by_name(self, name: str, exact: bool = False, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for entities by legal name (convenience method).
        
        Args:
            name: Entity name to search for
            exact: If True, search for exact match; if False, use wildcard search
            limit: Maximum number of results to return
            
        Returns:
            List of matching entity records
        """
        search_term = name if exact else f"*{name}*"
        results = self.search_lei_records("entity.legalName", search_term, size=limit)
        return results.get("data", [])

    def search_by_jurisdiction(self, country_code: str, limit: int = 25) -> List[Dict[str, Any]]:
        """Search for entities by jurisdiction (convenience method).
        
        Args:
            country_code: Two-letter country code (e.g., 'US', 'GB')
            limit: Maximum number of results to return
            
        Returns:
            List of entity records from the specified jurisdiction
        """
        results = self.search_lei_records("entity.jurisdiction", country_code.upper(), size=limit)
        return results.get("data", [])

    def get_entity_hierarchy(self, lei: str) -> Dict[str, Any]:
        """Get entity hierarchy information (convenience method).
        
        Args:
            lei: The 20-character LEI code
            
        Returns:
            Dictionary with entity record and parent information if available
        """
        record = self.get_lei_record(lei)
        result = {"entity": record}
        
        # Try to get parent information if available
        parent_info = record.get("entity", {}).get("parent")
        if parent_info and parent_info.get("lei"):
            try:
                parent_record = self.get_lei_record(parent_info["lei"])
                result["parent"] = parent_record
            except Exception:
                # Parent LEI might not be available or accessible
                result["parent"] = None
                
        return result


class AsyncGleifClient:
    """Asynchronous client for the GLEIF API.
    
    Similar to GleifClient but with async/await support for better performance
    in async applications.
    
    Example:
        >>> import asyncio
        >>> async def main():
        ...     async with AsyncGleifClient() as client:
        ...         record = await client.get_lei_record("529900T8BM49AURSDO55")
        ...         print(record['entity']['legalName'])
        >>> asyncio.run(main())
    """
    
    def __init__(
        self,
        base_url: str = GLEIF_BASE_URL,
        timeout: float = 30.0,
        user_agent: str = "gleif-mcp-client-async/0.1.0",
    ):
        """Initialize the async GLEIF client.
        
        Args:
            base_url: Base URL for the GLEIF API
            timeout: Request timeout in seconds
            user_agent: User agent string for requests
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = {
            "User-Agent": user_agent,
            "Accept": "application/json",
        }
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=self.timeout, headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    async def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make an asynchronous HTTP request to the GLEIF API.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            Parsed JSON response
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with AsyncGleifClient()' context manager.")
            
        url = _build_url(self.base_url, endpoint)
        response = await self._client.get(url, params=params or {})
        return _handle_response(response)

    async def get_lei_record(self, lei: str) -> Dict[str, Any]:
        """Async version of get_lei_record."""
        return await self._request(f"/lei-records/{quote(lei)}")

    async def search_lei_records(
        self,
        filter_key: str,
        filter_value: str,
        page: int = 1,
        size: int = 25,
    ) -> Dict[str, Any]:
        """Async version of search_lei_records."""
        params = {
            f"filter[{filter_key}]": filter_value,
            "page": page,
            "size": size,
        }
        return await self._request("/lei-records", params)

    # Add other async methods as needed following the same pattern...


# Module-level convenience functions
def get_lei_record(lei: str) -> Dict[str, Any]:
    """Get a LEI record (module-level convenience function).
    
    Args:
        lei: The 20-character LEI code
        
    Returns:
        Dictionary containing the LEI record
    """
    client = GleifClient()
    return client.get_lei_record(lei)


def search_lei_records(filter_key: str, filter_value: str, **kwargs) -> Dict[str, Any]:
    """Search LEI records (module-level convenience function).
    
    Args:
        filter_key: Field to filter on
        filter_value: Value to match
        **kwargs: Additional parameters (page, size)
        
    Returns:
        Dictionary containing search results
    """
    client = GleifClient()
    return client.search_lei_records(filter_key, filter_value, **kwargs)


def search_by_name(name: str, exact: bool = False, limit: int = 10) -> List[Dict[str, Any]]:
    """Search entities by name (module-level convenience function).
    
    Args:
        name: Entity name to search for
        exact: Whether to search for exact match
        limit: Maximum results to return
        
    Returns:
        List of matching entities
    """
    client = GleifClient()
    return client.search_by_name(name, exact, limit)