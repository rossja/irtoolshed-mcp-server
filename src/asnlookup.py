# asnlookup.py
import subprocess
from subprocess import CalledProcessError

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
        cmd_result = subprocess.run(
            ["whois", "-h", "whois.cymru.com", ip],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse the output - skip the header line and get the data line
        lines = cmd_result.stdout.strip().split('\n')
        if len(lines) >= 2:  # Make sure we have at least 2 lines (header + data)
            data_line = lines[1]  # Get the second line (index 1)
            parts = data_line.split('|')
            if len(parts) >= 3:
                result_dict["ip_addr"] = parts[1].strip()
                result_dict["as_number"] = parts[0].strip()
                result_dict["as_name"] = parts[2].strip()
    except (CalledProcessError, Exception):
        # The default error values are already set in result_dict
        pass

    return result_dict