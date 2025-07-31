"""Tests for the GLEIF API client."""

import pytest
from gleif_mcp.client import GleifClient

def test_client_instantiation():
    """Test that the GleifClient can be instantiated."""
    client = GleifClient()
    assert client is not None
