# asnlookup.py
import cymruwhois

def asnlookup(ip):
    """
    Look up ASN information for a given IP address and return formatted results.

    Args:
        ip: The IP address to look up

    Returns:
        dict: A dictionary with ip, as number, and as name
    """
    # Initialize the result dictionary with default values
    result_dict = {
        "ip_addr": ip,
        "as_number": "error",
        "as_name": "error"
    }

    try:
        # Use the cymruwhois library to get ASN information
        client = cymruwhois.Client()
        response = client.lookup(ip)

        # Update the result dictionary with the ASN information
        if response:
            result_dict["ip_addr"] = ip
            result_dict["as_number"] = str(response.asn)
            result_dict["as_name"] = response.owner
    except Exception as e:
        # The default error values are already set in result_dict
        print(f"Error looking up ASN for IP: {ip}")
        print(f"Exception: {str(e)}")

    return result_dict

if __name__ == "__main__":
    print(f"running asnlookup as main")
    result = asnlookup("8.8.8.8")
    print(f"Result: {result}")