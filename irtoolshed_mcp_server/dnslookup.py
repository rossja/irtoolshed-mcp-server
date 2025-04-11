# dnslookup.py
import dns.resolver
import dns.exception

def dnslookup(domain, record_type="A"):
    """
    Perform DNS lookups for a domain with specified record type.

    Args:
        domain: The domain name to look up
        record_type: The DNS record type (A, AAAA, MX, etc.)

    Returns:
        dict: A dictionary with domain, record type, and results or error information
    """
    try:
        # Sanitize inputs
        domain = domain.strip() if domain else ""
        record_type = record_type.strip().upper() if record_type else "A"
        
        # Validate record type
        valid_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "PTR"]
        if record_type not in valid_types:
            return {
                "status": "error",
                "error": f"Invalid record type. Must be one of: {', '.join(valid_types)}",
                "query": {"domain": domain, "record_type": record_type}
            }

        # Perform DNS query
        answers = dns.resolver.resolve(domain, record_type)
        
        # Process the results
        records = []
        for rdata in answers:
            if record_type == "MX":
                records.append({
                    "preference": rdata.preference,
                    "exchange": str(rdata.exchange)
                })
            else:
                records.append(str(rdata))
        
        return {
            "status": "success",
            "domain": domain,
            "record_type": record_type,
            "records": records
        }

    except dns.resolver.NXDOMAIN:
        return {
            "status": "error",
            "error": f"Domain {domain} does not exist",
            "query": {"domain": domain, "record_type": record_type}
        }
    except dns.resolver.NoAnswer:
        return {
            "status": "error",
            "error": f"No {record_type} records found for {domain}",
            "query": {"domain": domain, "record_type": record_type}
        }
    except dns.resolver.NoNameservers:
        return {
            "status": "error",
            "error": f"No nameservers available for {domain}",
            "query": {"domain": domain, "record_type": record_type}
        }
    except dns.exception.Timeout:
        return {
            "status": "error",
            "error": "DNS query timed out",
            "query": {"domain": domain, "record_type": record_type}
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "query": {"domain": domain, "record_type": record_type}
        }

if __name__ == "__main__":
    print("Running dnslookup as main")
    # Test A record
    result = dnslookup("google.com", "A")
    print(f"A Record Result: {result}")
    # Test MX record
    result = dnslookup("google.com", "MX")
    print(f"MX Record Result: {result}") 