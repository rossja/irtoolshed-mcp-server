import pytest
from irtoolshed_mcp_server.geolookup import geolookup, has_geoip_database
import os

def has_geoip_database():
    """Helper function to check if GeoIP database exists"""
    return any(os.path.exists(p) for p in [
        "GeoLite2-City.mmdb",
        "/usr/share/GeoIP/GeoLite2-City.mmdb",
        os.path.expanduser("~/.local/share/GeoIP/GeoLite2-City.mmdb")
    ])

def test_geolookup_google_dns():
    """Test geolocation lookup for Google's DNS server"""
    if not has_geoip_database():
        pytest.skip("GeoIP database not found")
    
    result = geolookup("8.8.8.8")
    assert result["status"] == "success"
    assert result["ip_addr"] == "8.8.8.8"
    assert result["raw_output"]  # Should have raw output
    assert result["country"] != "Unknown"  # Should find country
    assert result["city"] != "Unknown"  # Should find city
    assert "latitude" in result  # Should have coordinates
    assert "longitude" in result
    assert isinstance(result["latitude"], float)
    assert isinstance(result["longitude"], float)
    # Optional fields
    if "postal_code" in result:
        assert result["postal_code"] == "94043"
    if "region" in result:
        assert result["region"] == "California"
    if "asn" in result:
        assert result["asn"] == 15169
    if "as_org" in result:
        assert "Google" in result["as_org"]

def test_geolookup_google_dns_ipv6():
    """Test geolocation lookup for Google's IPv6 DNS server"""
    if not has_geoip_database():
        pytest.skip("GeoIP database not found")
    
    result = geolookup("2001:4860:4860::8888")
    assert result["status"] == "success"
    assert result["ip_addr"] == "2001:4860:4860::8888"
    assert result["raw_output"]  # Should have raw output
    assert result["country"] != "Unknown"  # Should find country
    assert "latitude" in result  # Should have coordinates
    assert "longitude" in result
    assert isinstance(result["latitude"], float)
    assert isinstance(result["longitude"], float)
    assert "America/" in result["timezone"]

def test_geolookup_cloudflare():
    """Test geolocation lookup for Cloudflare's DNS"""
    if not has_geoip_database():
        pytest.skip("GeoIP database not found")
    
    result = geolookup("1.1.1.1")
    assert result["status"] == "success"
    assert result["ip_addr"] == "1.1.1.1"
    assert result["raw_output"]  # Should have raw output
    assert result["country"] != "Unknown"  # Should find country
    assert "latitude" in result  # Should have coordinates
    assert "longitude" in result
    assert isinstance(result["latitude"], float)
    assert isinstance(result["longitude"], float)
    # Optional fields
    if "asn" in result:
        assert result["asn"] == 13335
    if "as_org" in result:
        assert "Cloudflare" in result["as_org"]

def test_geolookup_cloudflare_ipv6():
    """Test geolocation lookup for Cloudflare's IPv6 DNS"""
    if not has_geoip_database():
        pytest.skip("GeoIP database not found")
    
    result = geolookup("2606:4700:4700::1111")
    assert result["status"] == "success"
    assert result["ip_addr"] == "2606:4700:4700::1111"
    assert result["raw_output"]  # Should have raw output
    assert result["country"] != "Unknown"  # Should find country
    assert "latitude" in result  # Should have coordinates
    assert "longitude" in result
    assert isinstance(result["latitude"], float)
    assert isinstance(result["longitude"], float)
    assert result["timezone"] is not None

def test_geolookup_invalid_ip():
    """Test geolocation lookup with invalid IP"""
    result = geolookup("not-an-ip")
    assert result["status"] == "error"
    assert "Invalid IP address format" in result["error"]
    assert result["query"]["ip"] == "not-an-ip"

def test_geolookup_private_ip():
    """Test geolocation lookup with private IP"""
    result = geolookup("192.168.1.1")
    assert result["status"] == "error"
    assert "IP address not found in the database" in result["error"]
    assert result["query"]["ip"] == "192.168.1.1"

def test_geolookup_private_ipv6():
    """Test geolocation lookup with private IPv6"""
    result = geolookup("fd00::1")
    assert result["status"] == "error"
    assert "IP address not found in the database" in result["error"]
    assert result["query"]["ip"] == "fd00::1"

def test_geolookup_no_database():
    """Test geolocation lookup without database"""
    if has_geoip_database():
        pytest.skip("Cannot test missing database when database exists")
    
    result = geolookup("8.8.8.8")
    assert result["status"] == "error"
    assert "GeoIP2 database not found" in result["error"]
    assert result["query"]["ip"] == "8.8.8.8"

def test_geolookup_invalid_license():
    """Test geolocation lookup with invalid license key"""
    result = geolookup("8.8.8.8", license_key="invalid_key")
    assert result["status"] == "error"
    assert "Invalid license key" in result["error"]
    assert result["query"]["ip"] == "8.8.8.8" 