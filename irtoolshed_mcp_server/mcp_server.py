# mcp_server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("irtoolshed")

# Add prompts for each tool
@mcp.prompt()
def asnlookup_examples():
    """Examples for using the ASN lookup tool"""
    return """Here are some examples of using the ASN lookup tool:

# Look up Google's DNS server
asnlookup("8.8.8.8")

# Look up Cloudflare's DNS
asnlookup("1.1.1.1")

# Look up Google's IPv6 DNS
asnlookup("2001:4860:4860::8888")
"""

@mcp.prompt()
def dnslookup_examples():
    """Examples for using the DNS lookup tool"""
    return """Here are some examples of using the DNS lookup tool:

# Look up A records (IPv4)
dnslookup("google.com", "A")

# Look up AAAA records (IPv6)
dnslookup("google.com", "AAAA")

# Look up MX records (mail servers)
dnslookup("google.com", "MX")

# Look up NS records (nameservers)
dnslookup("google.com", "NS")

# Look up TXT records
dnslookup("google.com", "TXT")
"""

@mcp.prompt()
def whoislookup_examples():
    """Examples for using the WHOIS lookup tool"""
    return """Here are some examples of using the WHOIS lookup tool:

# Look up domain registration information
whoislookup("google.com")

# Look up a different TLD
whoislookup("bbc.co.uk")

# Look up a newer TLD
whoislookup("github.dev")
"""

@mcp.prompt()
def geolookup_examples():
    """Examples for using the geolocation lookup tool"""
    return """Here are some examples of using the geolocation lookup tool:

# Basic lookup using environment variable or interactive prompt
geolookup("8.8.8.8")

# Lookup with explicit license key
geolookup("8.8.8.8", license_key="your_maxmind_license_key")

# IPv6 address lookup
geolookup("2001:4860:4860::8888")

# Cloudflare's DNS
geolookup("1.1.1.1")

Note: If you haven't set up your MaxMind license key yet:
1. Get a free key from: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
2. Either:
   - Set the MAXMIND_LICENSE_KEY environment variable
   - Provide it as license_key parameter
   - Enter it when prompted
"""

# Add the asnlookup function to the server as a tool
@mcp.tool()
def asnlookup(ipaddr: str) -> str:
    from asnlookup import asnlookup
    """perform a lookup on an IP address to get the ASN and country"""
    return asnlookup(ipaddr)

# Add the dnslookup function to the server as a tool
@mcp.tool()
def dnslookup(domain: str, record_type: str = "A") -> str:
    from dnslookup import dnslookup
    """perform a DNS lookup for a domain with specified record type"""
    return dnslookup(domain, record_type)

# Add the whoislookup function to the server as a tool
@mcp.tool()
def whoislookup(domain: str) -> str:
    from whoislookup import whoislookup
    """perform a WHOIS lookup for a domain name"""
    return whoislookup(domain)

# Add the geolookup function to the server as a tool
@mcp.tool()
def geolookup(ipaddr: str, license_key: str = None) -> str:
    from geolookup import geolookup
    """perform a geolocation lookup for an IP address, optionally providing a MaxMind license key"""
    return geolookup(ipaddr, license_key)

# Add resources to provide documentation about the tools
@mcp.resource(name="asnlookup_documentation",
             uri="resource://asnlookup/documentation")
def asnlookup_doc():
    """Documentation for the asnlookup tool"""
    return """
    # ASN Lookup Tool Documentation

    ## Overview

    The asnlookup tool provides information about an IP address's
    Autonomous System Number (ASN) and related details.
    This tool is useful for network administrators and security
    professionals who need to identify the organization that owns a
    specific IP address or range of addresses.

    ## Usage

    Call the tool with an IP address (IPv4 or IPv6):

    ```python
    asnlookup("8.8.8.8")
    asnlookup("2001:4860:4860::8888")
    ```

    ## Output Format

    Success Response:
    ```json
    {
        "status": "success",
        "ip_addr": "8.8.8.8",
        "as_number": "15169",
        "as_name": "GOOGLE - Google LLC"
    }
    ```

    Error Response:
    ```json
    {
        "status": "error",
        "error": "Detailed error message",
        "query": "8.8.8.8"
    }
    ```

    Common error cases:
    - Invalid IP address format
    - No ASN information found (including private IP addresses)
    - Network connectivity issues
    """

@mcp.resource(name="dnslookup_documentation",
             uri="resource://dnslookup/documentation")
def dnslookup_doc():
    """Documentation for the dnslookup tool"""
    return """
    # DNS Lookup Tool Documentation

    ## Overview

    The dnslookup tool performs DNS queries for a domain name with
    support for various record types (A, AAAA, MX, etc.).

    ## Usage

    Call the tool with a domain name and optional record type:

    ```python
    dnslookup("google.com", "A")     # IPv4 address
    dnslookup("google.com", "AAAA")  # IPv6 address
    dnslookup("google.com", "MX")    # Mail servers
    dnslookup("google.com", "NS")    # Nameservers
    dnslookup("google.com", "TXT")   # Text records
    ```

    Supported record types: A, AAAA, MX, NS, TXT, CNAME, SOA, PTR

    ## Output Format

    Success Response:
    ```json
    {
        "status": "success",
        "domain": "google.com",
        "record_type": "A",
        "records": ["142.250.190.78"]
    }
    ```

    For MX records:
    ```json
    {
        "status": "success",
        "domain": "google.com",
        "record_type": "MX",
        "records": [
            {
                "preference": 10,
                "exchange": "smtp.google.com"
            }
        ]
    }
    ```

    Error Response:
    ```json
    {
        "status": "error",
        "error": "Detailed error message",
        "query": {
            "domain": "google.com",
            "record_type": "A"
        }
    }
    ```

    Common error cases:
    - Invalid record type
    - Domain does not exist
    - No records found
    - No nameservers available
    - DNS query timeout
    """

@mcp.resource(name="whoislookup_documentation",
             uri="resource://whoislookup/documentation")
def whoislookup_doc():
    """Documentation for the whoislookup tool"""
    return """
    # WHOIS Lookup Tool Documentation

    ## Overview

    The whoislookup tool retrieves WHOIS registration information
    for a domain name. It provides details about domain ownership,
    registration dates, and nameservers.

    ## Usage

    Call the tool with a domain name:

    ```python
    whoislookup("google.com")
    whoislookup("example.co.uk")
    ```

    ## Output Format

    Success Response:
    ```json
    {
        "status": "success",
        "domain": "example.com",
        "registrar": "Example Registrar, LLC",
        "registrant": "Example Organization",
        "creation_date": "2004-04-26 00:00:00",
        "expiration_date": "2025-04-26 00:00:00",
        "name_servers": ["ns1.example.com", "ns2.example.com"],
        "raw_output": "Raw WHOIS server response..."
    }
    ```

    Error Response:
    ```json
    {
        "status": "error",
        "error": "Detailed error message",
        "query": "example.com",
        "raw_output": "Raw error response if available"
    }
    ```

    Common error cases:
    - Invalid domain name format
    - Domain not found
    - WHOIS server not available
    - Rate limiting or access restrictions
    """

@mcp.resource(name="geolookup_documentation",
             uri="resource://geolookup/documentation")
def geolookup_doc():
    """Documentation for the geolookup tool"""
    return """
    # Geolocation Lookup Tool Documentation

    ## Overview

    The geolookup tool provides detailed geolocation information for IP addresses
    using MaxMind's GeoLite2 database. It includes country, city, coordinates,
    and network information.

    ## Prerequisites

    This tool requires a MaxMind GeoLite2 license key. You can:
    1. Get a free key from: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
    2. Either:
       - Set the MAXMIND_LICENSE_KEY environment variable
       - Provide it as a parameter when using the tool
       - Enter it when prompted

    ## Usage

    Basic usage (uses environment variable or prompts for key):
    ```python
    geolookup("8.8.8.8")
    ```

    With explicit license key:
    ```python
    geolookup("8.8.8.8", license_key="your_maxmind_license_key")
    ```

    ## Output Format

    Success Response:
    ```json
    {
        "status": "success",
        "ip_addr": "8.8.8.8",
        "raw_output": {
            "continent": {
                "code": "NA",
                "name": "North America"
            },
            "country": {
                "iso_code": "US",
                "name": "United States"
            },
            "city": {
                "name": "Mountain View",
                "confidence": 90
            },
            "location": {
                "latitude": 37.40599,
                "longitude": -122.078514,
                "accuracy_radius": 1000,
                "time_zone": "America/Los_Angeles"
            },
            "postal": {
                "code": "94043",
                "confidence": 90
            },
            "subdivisions": [{
                "iso_code": "CA",
                "name": "California",
                "confidence": 90
            }],
            "traits": {
                "autonomous_system_number": 15169,
                "autonomous_system_organization": "Google LLC",
                "ip_address": "8.8.8.8",
                "network": "8.8.8.0/24"
            }
        }
    }
    ```

    Error Response:
    ```json
    {
        "status": "error",
        "error": "Detailed error message",
        "query": {"ip": "8.8.8.8"}
    }
    ```

    Common error cases:
    - Invalid IP address format
    - Private IP address
    - Missing or invalid MaxMind license key
    - Database not found or download failed
    - IP not found in database
    """

def main():
    """Entry point for the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()