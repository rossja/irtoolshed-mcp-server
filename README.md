# IR Toolshed MCP Server

A comprehensive Model Context Protocol (MCP) server providing incident response
and network analysis tools for security professionals. This server allows AI
models like Claude to perform various network-related lookups and analyses to
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

More tools will be added in future releases.

## Prerequisites

- Python 3.8 or newer (3.13+ recommended)
- [uv](https://github.com/astral-sh/uv) Python package manager
- The `whois` command-line tool must be installed on your system

### Installing whois

#### On Ubuntu/Debian:
```bash
sudo apt-get install whois
```

#### On macOS:
```bash
brew install whois
```

#### On Windows:
Download a Windows whois tool or use WSL (Windows Subsystem for Linux).

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

## Error Handling

Each tool has its own error handling approach. Generally, tools will return
specific error fields or indicators when a lookup fails:

For the ASN lookup tool:
```json
{
    "ip_addr": "<queried-ip>",
    "as_number": "error",
    "as_name": "error"
}
```

## Project Structure

- `src/mcp_server.py`: The main MCP server implementation
- `src/asnlookup.py`: The ASN lookup functionality
- `src/__init__.py`: Makes the directory a Python package
- `pyproject.toml`: Project configuration and dependencies

## Roadmap

Future tools planned for inclusion:
- DNS record lookups (A, AAAA, MX, etc.)
- Reverse DNS lookups
- IP geolocation services
- WHOIS record retrieval
- Domain reputation scoring
- SSL certificate analysis

## Contributing

Contributions to add new IR tools or improve existing ones are welcome.
Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Add your tool following the existing pattern in mcp_server.py
4. Include appropriate documentation as a resource
5. Submit a pull request with a clear description of your changes

## License

[Add your license information here]

## Security Considerations

This server is intended for legitimate security research and incident response.
Users must ensure they comply with all applicable laws and regulations when
using these tools.