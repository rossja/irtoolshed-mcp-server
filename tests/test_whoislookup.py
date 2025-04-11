import pytest
from irtoolshed_mcp_server.whoislookup import whoislookup
from datetime import datetime

def test_whoislookup_google():
    """Test WHOIS lookup for google.com"""
    result = whoislookup("google.com")
    assert result["status"] == "success"
    assert result["domain"] == "google.com"
    assert result["raw_output"]  # Should have raw output
    assert result["registrar"] != "Unknown"  # Should find registrar
    assert "name_servers" in result
    assert len(result["name_servers"]) > 0
    # Verify all nameservers are google.com
    for ns in result["name_servers"]:
        assert "google" in ns.lower()
    # Verify dates are parseable
    assert datetime.strptime(result["creation_date"].split()[0], "%Y-%m-%d")
    assert datetime.strptime(result["expiration_date"].split()[0], "%Y-%m-%d")

def test_whoislookup_nonexistent_domain():
    """Test WHOIS lookup for nonexistent domain"""
    result = whoislookup("thisisnotarealdomain12345.com")
    assert result["status"] == "error"
    assert 'No match for "THISISNOTAREALDOMAIN12345.COM"' in result["error"]
    assert result["query"] == "thisisnotarealdomain12345.com"
    assert result["raw_output"]  # Should have raw output even for errors

def test_whoislookup_microsoft():
    """Test WHOIS lookup for microsoft.com"""
    result = whoislookup("microsoft.com")
    assert result["status"] == "success"
    assert result["domain"] == "microsoft.com"
    assert result["raw_output"]  # Should have raw output
    assert result["registrar"] != "Unknown"  # Should find registrar
    assert "name_servers" in result
    assert len(result["name_servers"]) > 0
    # Verify dates are parseable
    assert datetime.strptime(result["creation_date"].split()[0], "%Y-%m-%d")
    assert datetime.strptime(result["expiration_date"].split()[0], "%Y-%m-%d")

def test_whoislookup_invalid_input():
    """Test WHOIS lookup with invalid input"""
    result = whoislookup("not-a-domain")
    assert result["status"] == "error"
    assert "Invalid domain name format" in result["error"]
    assert result["query"] == "not-a-domain"

def test_whoislookup_co_uk():
    """Test WHOIS lookup for .co.uk domain"""
    result = whoislookup("bbc.co.uk")
    assert result["status"] == "success"
    assert result["domain"] == "bbc.co.uk"
    assert result["raw_output"]  # Should have raw output
    assert result["registrar"] != "Unknown"  # Should find registrar
    assert "name_servers" in result
    assert len(result["name_servers"]) > 0

def test_whoislookup_new_tld():
    """Test WHOIS lookup for newer TLD"""
    result = whoislookup("something.dev")
    assert result["status"] == "success"
    assert result["domain"] == "something.dev"
    assert result["raw_output"]  # Should have raw output
    # Don't make assumptions about other fields for new TLDs 