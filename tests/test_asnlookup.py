import pytest
from irtoolshed_mcp_server.asnlookup import asnlookup

def test_asnlookup_google_dns():
    """Test ASN lookup for Google's DNS server"""
    result = asnlookup("8.8.8.8")
    assert result["status"] == "success"
    assert result["ip_addr"] == "8.8.8.8"
    assert result["as_number"] == "15169"
    assert "GOOGLE" in result["as_name"]
    
def test_asnlookup_cloudflare():
    """Test ASN lookup for Cloudflare's DNS"""
    result = asnlookup("1.1.1.1")
    assert result["status"] == "success"
    assert result["ip_addr"] == "1.1.1.1"
    assert result["as_number"] == "13335"
    assert "CLOUDFLARENET" in result["as_name"]

def test_asnlookup_google_ipv6():
    """Test ASN lookup for Google's IPv6 address"""
    result = asnlookup("2001:4860:4860::8888")
    assert result["status"] == "success"
    assert result["ip_addr"] == "2001:4860:4860::8888"
    assert result["as_number"] == "15169"
    assert "GOOGLE" in result["as_name"]

def test_asnlookup_cloudflare_ipv6():
    """Test ASN lookup for Cloudflare's IPv6 DNS"""
    result = asnlookup("2606:4700:4700::1111")
    assert result["status"] == "success"
    assert result["ip_addr"] == "2606:4700:4700::1111"
    assert result["as_number"] == "13335"
    assert "CLOUDFLARENET" in result["as_name"]

def test_asnlookup_invalid_ip():
    """Test ASN lookup with invalid IP"""
    result = asnlookup("invalid.ip")
    assert result["status"] == "error"
    assert "Invalid IP address format" in result["error"]
    assert result["query"] == "invalid.ip"

def test_asnlookup_private_ip():
    """Test ASN lookup with private IP"""
    result = asnlookup("192.168.1.1")
    assert result["status"] == "error"
    assert "No ASN information found" in result["error"]
    assert result["query"] == "192.168.1.1"

def test_asnlookup_private_ipv6():
    """Test ASN lookup with private IPv6"""
    result = asnlookup("fd00::1")
    assert result["status"] == "error"
    assert "No ASN information found" in result["error"]
    assert result["query"] == "fd00::1" 