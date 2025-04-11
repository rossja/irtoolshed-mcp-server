# whoislookup.py
import whois
import re
from datetime import datetime

def is_valid_domain(domain):
    """Check if a domain name is valid."""
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))

def format_date(date_value):
    """Format a date value consistently."""
    if not date_value:
        return None
        
    if isinstance(date_value, list):
        date_value = date_value[0]
        
    if isinstance(date_value, (datetime, str)):
        return str(date_value).split('.')[0]  # Remove microseconds if present
        
    return None

def format_nameservers(nameservers):
    """Format nameservers consistently."""
    if not nameservers:
        return []
        
    if isinstance(nameservers, str):
        return [nameservers.lower()]
        
    if isinstance(nameservers, list):
        return [ns.lower() for ns in nameservers if ns and str(ns).strip()]
        
    return []

def whoislookup(domain):
    """
    Perform WHOIS lookup for a domain name.

    Args:
        domain: The domain name to look up

    Returns:
        dict: A dictionary with domain registration information or error details.
             Always includes raw_output for debugging and custom parsing.
    """
    try:
        # Sanitize input
        domain = domain.strip() if domain else ""
        
        # Validate domain format
        if not is_valid_domain(domain):
            return {
                "status": "error",
                "error": "Invalid domain name format",
                "query": domain,
                "raw_output": None
            }

        # Perform WHOIS query
        w = whois.whois(domain)
        
        # Store raw output
        raw_output = w.text

        # Check if the domain exists
        if not w.domain_name:
            return {
                "status": "error",
                "error": "Domain not found",
                "query": domain,
                "raw_output": raw_output
            }

        # Process the results with default "Unknown" for unmappable fields
        result = {
            "status": "success",
            "domain": domain,
            "registrar": "Unknown",
            "registrant": "Unknown",
            "creation_date": "Unknown",
            "expiration_date": "Unknown",
            "name_servers": [],
            "raw_output": raw_output
        }

        # Try to map known fields
        if w.registrar:
            registrar = w.registrar[0] if isinstance(w.registrar, list) else w.registrar
            if registrar and str(registrar).strip():
                result["registrar"] = registrar

        if w.creation_date:
            creation_date = format_date(w.creation_date)
            if creation_date:
                result["creation_date"] = creation_date

        if w.expiration_date:
            expiration_date = format_date(w.expiration_date)
            if expiration_date:
                result["expiration_date"] = expiration_date

        if w.name_servers:
            result["name_servers"] = format_nameservers(w.name_servers)

        # Try to map registrant (but don't try too hard)
        if hasattr(w, 'registrant') and w.registrant:
            registrant = w.registrant[0] if isinstance(w.registrant, list) else w.registrant
            if registrant and str(registrant).strip():
                result["registrant"] = registrant
        elif hasattr(w, 'org') and w.org:
            org = w.org[0] if isinstance(w.org, list) else w.org
            if org and str(org).strip():
                result["registrant"] = org

        return result

    except whois.parser.PywhoisError as e:
        return {
            "status": "error",
            "error": str(e),
            "query": domain,
            "raw_output": getattr(e, 'text', None)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "query": domain,
            "raw_output": None
        }

if __name__ == "__main__":
    print("Running whoislookup as main")
    result = whoislookup("google.com")
    print(f"Result: {result}") 