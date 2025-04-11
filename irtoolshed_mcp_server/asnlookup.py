# asnlookup.py
import cymruwhois
import ipaddress

def is_private_ip(ip):
    """Check if an IP address is private"""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False

def asnlookup(ip):
    """
    Look up ASN information for a given IP address and return formatted results.

    Args:
        ip: The IP address to look up

    Returns:
        dict: A dictionary with ip, as number, and as name, or error information
    """
    try:
        # Sanitize input
        ip = ip.strip() if ip else ""
        
        # Validate IP address format
        ip_obj = ipaddress.ip_address(ip)
        
        # Check if it's a private IP
        if ip_obj.is_private:
            return {
                "status": "error",
                "error": "No ASN information found",
                "query": ip
            }
            
        # Use the cymruwhois library to get ASN information
        client = cymruwhois.Client()
        response = client.lookup(ip)

        if response:
            return {
                "status": "success",
                "ip_addr": ip,
                "as_number": str(response.asn),
                "as_name": response.owner
            }
        else:
            return {
                "status": "error",
                "error": "No ASN information found",
                "query": ip
            }
            
    except ValueError:
        return {
            "status": "error",
            "error": "Invalid IP address format",
            "query": ip
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "query": ip
        }

if __name__ == "__main__":
    print("Running asnlookup as main")
    result = asnlookup("8.8.8.8")
    print(f"Result: {result}")