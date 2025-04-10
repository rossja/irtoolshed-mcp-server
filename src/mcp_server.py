# mcp_server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("asnlookup")

# Add the asnlookup function to the server as a tool
@mcp.tool()
def asnlookup(ipaddr: str) -> str:
    from asnlookup import asnlookup
    """perform a lookup on an IP address to get the ASN and country"""
    return asnlookup(ipaddr)

# Add a resource to provide documentation about the asnlookup tool
@mcp.resource(name="asnlookup_documentation",
             uri="resource://asnlookup/documentation")
def asnlookup_doc():
    """
    Documentation for the asnlookup tool
    """
    return """
    # ASN Lookup Tool Documentation

    ## Overview

    The asnlookup tool provides information about an IP address's
    Autonomous System Number (ASN) and related details.
    This tool is useful for network administrators and security
    professionals who need to identify the organization that owns a
    specific IP address or range of addresses.

    It uses the whois.cymru.com service to retrieve this information.
    Both IPv4 and IPv6 addresses are supported.

    ## Usage

    Call the tool with an IP address:

    ```
    asnlookup("8.8.8.8")
    ```

    ## Output Format

    The tool returns a python dictionary with the following fields:

    - `ip_addr`: The IP address that was queried
    - `as_number`: The AS number associated with the IP address
    - `as_name`: The name of the organization that owns the AS number

    ## Example Output

    When you call the tool with a valid IP address, you will receive a
    response like:

    ```
    {
        "ip_addr": "8.8.8.8",
        "as_number": "15169",
        "as_name": "GOOGLE - Google LLC"
    }
    ```

    ## Error Handling

    If an error occurs during the lookup, the as_number and as_name fields
    will contain the string "error".

    ```
    {
        "ip_addr": "invalid_ip",
        "as_number": "error",
        "as_name": "error"
    }
    ```
    """

def main():
    """Entry point for the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()