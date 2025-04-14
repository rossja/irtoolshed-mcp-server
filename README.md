# IR Toolshed MCP Server

A comprehensive Model Context Protocol (MCP) server providing incident response
and network analysis tools for security professionals. This server allows AI
agents like Claude to perform various network-related lookups and analyses to
assist with security investigations.

## Overview

The IR Toolshed MCP Server provides a suite of networking and security tools
accessible via the Model Context Protocol. It's designed to be a general-purpose
service for network incident responders, enabling them to perform basic lookups
using:

- ASN (Autonomous System Number) lookups
- DNS lookups and analysis
- WHOIS record retrieval
- IP geolocation
- And more network analysis capabilities to come

Each tool is accompanied by detailed documentation as a resource, making it
easy for AI systems to understand how to use the tools and what output to
expect.

## Current Tools

### ASN Lookup Tool

The ASN lookup tool returns information about an IP address including:
- The IP address that was queried
- The AS number associated with the IP address
- The name of the organization that owns the AS number

### DNS Lookup Tool

The DNS lookup tool provides DNS record information for domains:
- Supports multiple record types (A, AAAA, MX, NS, TXT)
- Returns formatted DNS records
- Handles both IPv4 and IPv6 queries

### WHOIS Lookup Tool

The WHOIS lookup tool retrieves domain registration information:
- Domain ownership details
- Registration dates
- Nameserver information
- Registrar details

### Geolocation Tool

The IP geolocation tool provides location information using MaxMind's GeoLite2 database:
- Country and city-level location data
- Latitude and longitude coordinates
- Network information
- Timezone data

Note: The geolocation tool requires a MaxMind license key. You can:
1. Get a free key from: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
2. Either:
   - Set the MAXMIND_LICENSE_KEY environment variable
   - Provide it as a parameter when using the tool
   - Enter it when prompted

More tools will be added in future releases.

## Prerequisites

- Python 3.8 or newer (3.13+ recommended)
- [uv](https://github.com/astral-sh/uv) Python package manager

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd ir-toolshed-mcp-server
```

2. Create a virtual environment:
```bash
uv venv
```

3. Activate the virtual environment:

#### On Windows:
```bash
.venv\Scripts\activate
```

#### On macOS/Linux:
```bash
source .venv/bin/activate
```

4. Install the package in development mode:
```bash
uv pip install -e .
```

## Running the Server

Start the MCP server with:

```bash
uv run mcp dev src/mcp_server.py
```

This will launch the server in development mode, making it available to MCP
clients like Claude Desktop.

## Using the Tools

### ASN Lookup Tool

When connected to an MCP client such as Claude Desktop, you can use the ASN
lookup tool by providing an IP address:

```
asnlookup("8.8.8.8")
```

Example output:
```json
{
    "ip_addr": "8.8.8.8",
    "as_number": "15169",
    "as_name": "GOOGLE - Google LLC"
}
```

### DNS Lookup Tool

When connected to an MCP client such as Claude Desktop, you can use the DNS
lookup tool by providing a domain:

```
dnslookup("example.com")
```

Example output:
```json
{
    "domain": "example.com",
    "record_type": "A",
    "record_value": "93.184.216.34"
}
```

### WHOIS Lookup Tool

When connected to an MCP client such as Claude Desktop, you can use the WHOIS
lookup tool by providing a domain:

```
whoislookup("example.com")
```

Example output:
```json
{
    "domain": "example.com",
    "ownership_details": "Google LLC",
    "registration_date": "2004-04-26",
    "nameserver_information": "ns1.google.com",
    "registrar_details": "MarkMonitor Inc."
}
```

### Geolocation Tool

When connected to an MCP client such as Claude Desktop, you can use the geolocation
tool by providing an IP address:

```
geolocation("8.8.8.8")
```

Example output:
```json
{
    "ip_addr": "8.8.8.8",
    "country": "US",
    "city": "Mountain View",
    "latitude": 37.40599,
    "longitude": -122.078514,
    "network": "AS15169 Google LLC",
    "timezone": "America/Los_Angeles"
}
```

## Error Handling

Each tool follows a consistent error handling pattern:

General error response format:
```json
{
    "status": "error",
    "error": "Detailed error message",
    "query": "Original query value"
}
```

Tool-specific error examples:

ASN Lookup:
```json
{
    "ip_addr": "<queried-ip>",
    "status": "error",
    "error": "Invalid IP address format"
}
```

DNS Lookup:
```json
{
    "domain": "<queried-domain>",
    "record_type": "<requested-type>",
    "status": "error",
    "error": "DNS resolution failed"
}
```

WHOIS Lookup:
```json
{
    "domain": "<queried-domain>",
    "status": "error",
    "error": "WHOIS server not available"
}
```

Geolocation:
```json
{
    "ip_addr": "<queried-ip>",
    "status": "error",
    "error": "MaxMind database not found or license key invalid"
}
```

## Project Structure

The project follows a standard Python package structure:

```
irtoolshed_mcp_server/     # Main package directory
├── __init__.py           # Package initialization
├── asnlookup.py         # ASN lookup functionality
├── dnslookup.py         # DNS lookup functionality
├── geolookup.py         # Geolocation functionality
├── mcp_server.py        # Main MCP server implementation
└── whoislookup.py       # WHOIS lookup functionality

tests/                    # Test directory
├── test_asnlookup.py    # ASN lookup tests
├── test_dnslookup.py    # DNS lookup tests
├── test_geolookup.py    # Geolocation tests
└── test_whoislookup.py  # WHOIS lookup tests
```

## Development

### Setting Up Development Environment

1. Clone this repository:
```bash
git clone <repository-url>
cd ir-toolshed-mcp-server
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### Running Tests

To run the test suite:
```bash
uv run pytest
```

This will:
- Run all tests in the `tests/` directory
- Show test coverage information
- Display detailed output for any failures

Note: Some tests require additional configuration:
- Geolocation tests require a MaxMind GeoLite2 database and license key
- WHOIS tests may fail if the WHOIS service is unavailable

### Code Quality

The project uses several tools to maintain code quality:

- Format code with Black:
```bash
uv run black .
```

- Sort imports with isort:
```bash
uv run isort .
```

- Run type checking with mypy:
```bash
uv run mypy .
```

- Run linting with ruff:
```bash
uv run ruff .
```

## Roadmap

Completed:
✓ ASN lookups
✓ DNS record lookups (A, AAAA, MX, etc.)
✓ WHOIS record retrieval
✓ IP geolocation services

Future tools planned for inclusion:
- Domain reputation scoring
- SSL certificate analysis
- Network port scanning
- Threat intelligence integration
- Passive DNS history
- Email security analysis (SPF, DKIM, DMARC)
- BGP route analysis
- Network traffic visualization
- Malware hash lookups
- URL reputation checking

## Contributing

Contributions to add new IR tools or improve existing ones are welcome.
Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Add your tool following the existing pattern in mcp_server.py
4. Include appropriate documentation as a resource
5. Submit a pull request with a clear description of your changes

## License

Apache 2.0

## Security Considerations

This server is intended for legitimate security research and incident response.
Users must ensure they comply with all applicable laws and regulations when
using these tools.
