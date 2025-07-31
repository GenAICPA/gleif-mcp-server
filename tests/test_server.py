"""Tests for the GLEIF MCP server.
This module contains unit tests and integration tests for the GLEIF MCP server.
Tests are organized by functionality and use pytest fixtures for setup.
"""
import pytest
from unittest.mock import Mock, patch
from gleif_mcp._gleif_client import _build_url, _handle_response, _request
import httpx

class TestGleifClient:
    """Test the internal GLEIF client helper functions."""
    
    def test_build_url_basic(self):
        """Test basic URL building."""
        url = _build_url("https://api.gleif.org/api/v1", "/lei-records")
        assert url == "https://api.gleif.org/api/v1/lei-records"
    
    def test_build_url_with_trailing_slash(self):
        """Test URL building with trailing slash in base."""
        url = _build_url("https://api.gleif.org/api/v1/", "/lei-records")
        assert url == "https://api.gleif.org/api/v1//lei-records"
    
    def test_handle_response_success(self):
        """Test successful response handling."""
        mock_response = Mock(spec=httpx.Response)
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": [{"lei": "test"}]}
        
        result = _handle_response(mock_response)
        assert result == {"data": [{"lei": "test"}]}
    
    def test_handle_response_http_error(self):
        """Test HTTP error response handling."""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404", request=Mock(), response=mock_response
        )
        
        result = _handle_response(mock_response)
        assert "error" in result
        assert "404" in result["error"]
    
    @patch('gleif_mcp._gleif_client.httpx.Client')
    def test_request_success(self, mock_client_class):
        """Test successful API request."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": []}
        
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client
        
        result = _request("/lei-records")
        assert result == {"data": []}
        mock_client.get.assert_called_once()
    
    @patch('gleif_mcp._gleif_client.httpx.Client')
    def test_request_with_params(self, mock_client_class):
        """Test API request with parameters."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": []}
        
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client
        
        params = {"page[number]": 1, "page[size]": 25}
        result = _request("/lei-records", params)
        
        mock_client.get.assert_called_once_with(
            "https://api.gleif.org/api/v1/lei-records", 
            params=params
        )


class TestServerTools:
    """Test the MCP server tools."""
    
    @patch('gleif_mcp.server._request')
    def test_list_lei_records(self, mock_request):
        """Test list_lei_records tool."""
        from gleif_mcp.server import list_lei_records
        
        mock_request.return_value = {"data": [{"lei": "test"}]}
        result = list_lei_records()
        
        mock_request.assert_called_once_with(
            "/lei-records", 
            {"page[number]": 1, "page[size]": 25}
        )
        assert result == {"data": [{"lei": "test"}]}
    
    @patch('gleif_mcp.server._request')
    def test_get_lei_record(self, mock_request):
        """Test get_lei_record tool."""
        from gleif_mcp.server import get_lei_record
        
        mock_request.return_value = {"data": {"lei": "529900T8BM49AURSDO55"}}
        result = get_lei_record("529900T8BM49AURSDO55")
        
        mock_request.assert_called_once_with("/lei-records/529900T8BM49AURSDO55")
        assert result["data"]["lei"] == "529900T8BM49AURSDO55"
    
    @patch('gleif_mcp.server._request')
    def test_search_lei_records(self, mock_request):
        """Test search_lei_records tool."""
        from gleif_mcp.server import search_lei_records
        
        mock_request.return_value = {"data": []}
        result = search_lei_records("entity.legalName", "Apple")
        
        expected_params = {
            "filter[entity.legalName]": "Apple",
            "page[number]": 1,
            "page[size]": 25
        }
        mock_request.assert_called_once_with("/lei-records", expected_params)


if __name__ == "__main__":
    pytest.main([__file__])