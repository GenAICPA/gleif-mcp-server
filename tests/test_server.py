"""Tests for the GLEIF MCP server.

This module contains unit tests and integration tests for the GLEIF MCP server.
Tests are organized by functionality and use pytest fixtures for setup.
"""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

from gleif_mcp.server import create_app
from gleif_mcp._gleif_client import _build_url, _handle_response


class TestGleifClient:
    """Test the internal GLEIF client helper functions."""
    
    def test_build_url_basic(self):
        """Test basic URL building."""
        url = _build_url("https://api.gleif.org/api/v1", "/lei-records")
        assert url == "https://api.gleif.org/api/v1/lei-records"
    
    def test_build_url_with_trailing_slash(self):
        """Test URL building with trailing slash in base URL."""
        url = _build_url("https://api.gleif.org/api/v1/", "/lei-records")
        assert url == "https://api.gleif.org/api/v1/lei-records"
    
    def test_build_url_without_leading_slash(self):
        """Test URL building without leading slash in endpoint."""
        url = _build_url("https://api.gleif.org/api/v1", "lei-records")
        assert url == "https://api.gleif.org/api/v1/lei-records"

    def test_handle_response_success(self):
        """Test successful response handling."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [], "meta": {"totalCount": 0}}
        mock_response.raise_for_status.return_value = None
        
        result = _handle_response(mock_response)
        assert result == {"data": [], "meta": {"totalCount": 0}}
        mock_response.raise_for_status.assert_called_once()

    def test_handle_response_http_error(self):
        """Test response handling with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("Not Found")
        
        with pytest.raises(Exception, match="Not Found"):
            _handle_response(mock_response)


class TestMCPServer:
    """Test the FastAPI MCP server endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client for the FastAPI app."""
        app = create_app()
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "service": "gleif-mcp-server"}

    def test_root_endpoint(self, client):
        """Test the root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["name"] == "GLEIF MCP Server"

    @patch('gleif_mcp._gleif_client._request')
    def test_list_lei_records(self, mock_request, client):
        """Test listing LEI records with mocked API."""
        mock_request.return_value = {
            "data": [
                {
                    "lei": "529900T8BM49AURSDO55",
                    "entity": {"legalName": "Test Entity"}
                }
            ],
            "meta": {"totalCount": 1}
        }
        
        response = client.get("/lei-records")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 1
        assert data["data"][0]["lei"] == "529900T8BM49AURSDO55"

    @patch('gleif_mcp._gleif_client._request')
    def test_get_lei_record(self, mock_request, client):
        """Test getting a specific LEI record."""
        test_lei = "529900T8BM49AURSDO55"
        mock_request.return_value = {
            "lei": test_lei,
            "entity": {
                "legalName": "Test Entity Inc.",
                "jurisdiction": "US"
            }
        }
        
        response = client.get(f"/lei-records/{test_lei}")
        assert response.status_code == 200
        data = response.json()
        assert data["lei"] == test_lei
        assert data["entity"]["legalName"] == "Test Entity Inc."

    def test_get_lei_record_invalid_format(self, client):
        """Test getting LEI record with invalid format."""
        response = client.get("/lei-records/INVALID")
        assert response.status_code == 400
        assert "Invalid LEI format" in response.json()["detail"]

    @patch('gleif_mcp._gleif_client._request')
    def test_search_lei_records(self, mock_request, client):
        """Test searching LEI records."""
        mock_request.return_value = {
            "data": [
                {
                    "lei": "529900T8BM49AURSDO55",
                    "entity": {"legalName": "Apple Inc."}
                }
            ],
            "meta": {"totalCount": 1}
        }
        
        response = client.get("/lei-records", params={
            "filter[entity.legalName]": "*Apple*"
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1

    @patch('gleif_mcp._gleif_client._request')
    def test_fuzzy_completions(self, mock_request, client):
        """Test fuzzy completion endpoint."""
        mock_request.return_value = {
            "data": ["Apple Inc.", "Apple Computer Inc."],
            "meta": {"totalCount": 2}
        }
        
        response = client.get("/lei-records/fuzzy-completions", params={
            "field": "entity.legalName",
            "q": "Apple"
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2


class TestLiveAPI:
    """Integration tests that hit the live GLEIF API.
    
    These tests are marked with @pytest.mark.live and are skipped by default
    in CI environments to avoid hitting rate limits.
    """
    
    @pytest.mark.live
    def test_live_list_lei_records(self):
        """Test listing LEI records from live API."""
        from gleif_mcp._gleif_client import _request
        
        response = _request("/lei-records", {"size": "5"})
        assert "data" in response
        assert "meta" in response
        assert len(response["data"]) <= 5

    @pytest.mark.live  
    def test_live_get_known_lei(self):
        """Test getting a known LEI from live API."""
        from gleif_mcp._gleif_client import _request
        
        # This is Apple Inc.'s LEI - should be stable
        test_lei = "HWUPKR0MPOU8FGXBT394"
        response = _request(f"/lei-records/{test_lei}")
        
        assert response["lei"] == test_lei
        assert "entity" in response
        assert "legalName" in response["entity"]

    @pytest.mark.live
    def test_live_search_apple(self):
        """Test searching for Apple entities from live API."""
        from gleif_mcp._gleif_client import _request
        
        params = {"filter[entity.legalName]": "*Apple*", "size": "5"}
        response = _request("/lei-records", params)
        
        assert "data" in response
        assert len(response["data"]) > 0
        
        # Check that results contain "Apple" in the name
        for record in response["data"]:
            legal_name = record["entity"]["legalName"].lower()
            assert "apple" in legal_name

    @pytest.mark.live
    def test_live_get_countries(self):
        """Test getting country list from live API."""
        from gleif_mcp._gleif_client import _request
        
        response = _request("/countries", {"size": "10"})
        assert "data" in response
        assert len(response["data"]) <= 10
        
        # Check structure of country data
        if response["data"]:
            country = response["data"][0]
            assert "code" in country
            assert "name" in country


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        app = create_app()
        return TestClient(app)

    def test_invalid_lei_format(self, client):
        """Test handling of invalid LEI format."""
        response = client.get("/lei-records/TOOLONG123456789012345")
        assert response.status_code == 400
        assert "Invalid LEI format" in response.json()["detail"]

    def test_missing_required_param(self, client):
        """Test handling of missing required parameters."""
        response = client.get("/lei-records/fuzzy-completions")
        assert response.status_code == 422  # Validation error

    @patch('gleif_mcp._gleif_client._request')
    def test_api_error_handling(self, mock_request, client):
        """Test handling of API errors."""
        mock_request.side_effect = Exception("API Error")
        
        response = client.get("/lei-records")
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]


class TestValidation:
    """Test input validation."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        app = create_app()
        return TestClient(app)

    def test_pagination_validation(self, client):
        """Test pagination parameter validation."""
        # Test negative page
        response = client.get("/lei-records", params={"page": "-1"})
        assert response.status_code == 422
        
        # Test zero page
        response = client.get("/lei-records", params={"page": "0"})
        assert response.status_code == 422
        
        # Test oversized page size
        response = client.get("/lei-records", params={"size": "1000"})
        assert response.status_code == 422

    def test_lei_format_validation(self, client):
        """Test LEI format validation."""
        valid_lei = "529900T8BM49AURSDO55"
        invalid_leis = [
            "123",  # too short
            "529900T8BM49AURSDO55TOOLONG",  # too long
            "529900T8BM49AURSDO5",  # 19 chars
            "529900T8BM49AURSDO555",  # 21 chars
            "529900t8bm49aursdo55",  # lowercase
            "529900T8BM49AURSDO5$",  # invalid character
        ]
        
        # Valid LEI should pass validation
        with patch('gleif_mcp._gleif_client._request') as mock_request:
            mock_request.return_value = {"lei": valid_lei, "entity": {}}
            response = client.get(f"/lei-records/{valid_lei}")
            assert response.status_code == 200
        
        # Invalid LEIs should fail validation
        for invalid_lei in invalid_leis:
            response = client.get(f"/lei-records/{invalid_lei}")
            assert response.status_code == 400, f"LEI {invalid_lei} should be invalid"


# Pytest configuration and fixtures
@pytest.fixture(scope="session")
def test_lei():
    """Provide a known valid LEI for testing."""
    return "HWUPKR0MPOU8FGXBT394"  # Apple Inc.

@pytest.fixture(scope="session") 
def test_country_code():
    """Provide a known valid country code for testing."""
    return "US"

@pytest.fixture(scope="session")
def test_issuer_id():
    """Provide a known valid issuer ID for testing."""
    return "1"  # First issuer in the system