import pytest
from irtoolshed_mcp_server.dnslookup import dnslookup
import re
import ipaddress

def is_valid_ipv6(address):
    """Helper function to validate IPv6 address format"""
    try:
        ipaddress.IPv6Address(address)
        return True
    except ipaddress.AddressValueError:
        return False

def test_dnslookup_a_record():
    """Test A record lookup"""
    result = dnslookup("google.com", "A")
    assert result["status"] == "success"
    assert result["domain"] == "google.com"
    assert result["record_type"] == "A"
    assert len(result["records"]) > 0
    # Verify each record is a valid IPv4 address
    for record in result["records"]:
        assert len(record.split(".")) == 4

def test_dnslookup_aaaa_record():
    """Test AAAA record lookup"""
    result = dnslookup("google.com", "AAAA")
    assert result["status"] == "success"
    assert result["domain"] == "google.com"
    assert result["record_type"] == "AAAA"
    assert len(result["records"]) > 0
    # Verify each record is a valid IPv6 address
    for record in result["records"]:
        assert is_valid_ipv6(record), f"Invalid IPv6 address format: {record}"

def test_dnslookup_aaaa_record_cloudflare():
    """Test AAAA record lookup for Cloudflare"""
    result = dnslookup("cloudflare.com", "AAAA")
    assert result["status"] == "success"
    assert result["domain"] == "cloudflare.com"
    assert result["record_type"] == "AAAA"
    assert len(result["records"]) > 0
    # Verify each record is a valid IPv6 address
    for record in result["records"]:
        assert is_valid_ipv6(record), f"Invalid IPv6 address format: {record}"

def test_dnslookup_mx_record():
    """Test MX record lookup"""
    result = dnslookup("google.com", "MX")
    assert result["status"] == "success"
    assert result["domain"] == "google.com"
    assert result["record_type"] == "MX"
    assert len(result["records"]) > 0
    # Verify each record has preference and exchange
    for record in result["records"]:
        assert "preference" in record
        assert "exchange" in record
        assert "google" in record["exchange"].lower()

def test_dnslookup_nonexistent_domain():
    """Test lookup for non-existent domain"""
    result = dnslookup("nonexistent.example.invalid", "A")
    assert result["status"] == "error"
    assert "Domain nonexistent.example.invalid does not exist" in result["error"]
    assert result["query"] == {"domain": "nonexistent.example.invalid", "record_type": "A"}

def test_dnslookup_nonexistent_domain_aaaa():
    """Test AAAA lookup for non-existent domain"""
    result = dnslookup("nonexistent.example.invalid", "AAAA")
    assert result["status"] == "error"
    assert "Domain nonexistent.example.invalid does not exist" in result["error"]
    assert result["query"] == {"domain": "nonexistent.example.invalid", "record_type": "AAAA"}

def test_dnslookup_invalid_record_type():
    """Test lookup with invalid record type"""
    result = dnslookup("google.com", "INVALID")
    assert result["status"] == "error"
    assert "Invalid record type" in result["error"]
    assert result["query"] == {"domain": "google.com", "record_type": "INVALID"}

def test_dnslookup_ipv6_only_domain():
    """Test lookup for an IPv6-only domain if available"""
    # ipv6.google.com is a domain known to have AAAA records
    result = dnslookup("ipv6.google.com", "AAAA")
    assert result["status"] == "success"
    assert result["domain"] == "ipv6.google.com"
    assert result["record_type"] == "AAAA"
    assert len(result["records"]) > 0
    # Verify each record is a valid IPv6 address
    for record in result["records"]:
        assert is_valid_ipv6(record), f"Invalid IPv6 address format: {record}"

def test_dnslookup_no_records():
    """Test lookup when no records are found"""
    result = dnslookup("google.com", "PTR")
    assert result["status"] == "error"
    assert "No PTR records found for google.com" in result["error"]
    assert result["query"] == {"domain": "google.com", "record_type": "PTR"} 