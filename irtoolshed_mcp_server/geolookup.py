# geolookup.py
import geoip2.database
import os
import tarfile
import requests
import shutil
from pathlib import Path
import ipaddress

# Constants for database management
MAXMIND_LICENSE_KEY_ENV = "MAXMIND_LICENSE_KEY"
GEOIP_DB_FILENAME = "GeoLite2-City.mmdb"
GEOIP_DB_PATHS = [
    GEOIP_DB_FILENAME,
    "/usr/share/GeoIP/" + GEOIP_DB_FILENAME,
    os.path.expanduser("~/.local/share/GeoIP/" + GEOIP_DB_FILENAME)
]

REGISTRATION_INSTRUCTIONS = """
To use the geolocation service, you need a free MaxMind GeoLite2 license key.
To obtain one:

1. Go to https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
2. Click "Sign Up for GeoLite2" and create an account
3. Once logged in, go to "My License Key" under your account
4. Generate a new license key

You can either:
- Set the MAXMIND_LICENSE_KEY environment variable, or
- Enter the key when prompted
"""

def get_license_key():
    """
    Get MaxMind license key from environment or user input.
    Provides registration instructions if needed.
    
    Returns:
        str: License key if provided, None otherwise
    """
    # First check environment variable
    license_key = os.getenv(MAXMIND_LICENSE_KEY_ENV)
    if license_key:
        return license_key
    
    # If not in environment, print instructions and ask user
    print("\nMaxMind license key not found in environment.")
    print(REGISTRATION_INSTRUCTIONS)
    
    # Prompt user for key
    print("\nDo you have a MaxMind license key? (yes/no)")
    response = input().lower().strip()
    
    if response == 'yes':
        print("\nPlease enter your MaxMind license key:")
        license_key = input().strip()
        
        # Ask if they want to save it
        print("\nWould you like to save this key to your environment? (yes/no)")
        save_response = input().lower().strip()
        if save_response == 'yes':
            # Write to .env file in user's home directory
            env_file = os.path.expanduser("~/.env")
            with open(env_file, 'a') as f:
                f.write(f'\nMAXMIND_LICENSE_KEY="{license_key}"\n')
            print(f"\nLicense key saved to {env_file}")
            print("To use it, add this to your shell's rc file (e.g., .zshrc, .bashrc):")
            print('export $(cat ~/.env | grep MAXMIND_LICENSE_KEY)')
        
        return license_key
    
    print("\nPlease register for a free license key and try again.")
    return None

def download_database(license_key=None):
    """
    Download and set up the MaxMind GeoLite2 City database.
    
    Args:
        license_key: Optional MaxMind license key. If not provided, will look for MAXMIND_LICENSE_KEY env var
                    or prompt the user.
    
    Returns:
        str: Path to the database file if successful, None if failed
    """
    try:
        # Create ~/.local/share/GeoIP directory if it doesn't exist
        db_dir = os.path.expanduser("~/.local/share/GeoIP")
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, GEOIP_DB_FILENAME)

        # Download the database
        url = f"https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key={license_key}&suffix=tar.gz"
        print("\nDownloading GeoLite2 City database...")
        response = requests.get(url)
        
        if response.status_code == 401:
            print("\nError: Invalid MaxMind license key")
            return None
            
        response.raise_for_status()

        # Save and extract the database
        tar_path = os.path.join(db_dir, "geolite2-city.tar.gz")
        with open(tar_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

        # Extract the .mmdb file from the tar.gz
        with tarfile.open(tar_path) as tar:
            for member in tar.getmembers():
                if member.name.endswith(GEOIP_DB_FILENAME):
                    member.name = os.path.basename(member.name)
                    tar.extract(member, db_dir)
                    extracted_db = os.path.join(db_dir, member.name)
                    # Move to final location if needed
                    if extracted_db != db_path:
                        shutil.move(extracted_db, db_path)
                    break

        # Clean up
        os.remove(tar_path)
        print(f"Database downloaded and installed to {db_path}")
        return db_path

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("\nError: Invalid MaxMind license key")
        else:
            print(f"\nError downloading database: {str(e)}")
        return None
    except Exception as e:
        print(f"\nError downloading database: {str(e)}")
        return None

def has_geoip_database():
    """Check if GeoIP database exists in any of the standard locations."""
    db_paths = [
        GEOIP_DB_FILENAME,
        "/usr/share/GeoIP/GeoLite2-City.mmdb",
        os.path.expanduser("~/.local/share/GeoIP/GeoLite2-City.mmdb")
    ]
    return any(os.path.exists(p) for p in db_paths)

def find_or_download_database(license_key=None):
    """Find existing database or download if not found."""
    # Check common locations
    db_paths = [
        GEOIP_DB_FILENAME,
        "/usr/share/GeoIP/GeoLite2-City.mmdb",
        os.path.expanduser("~/.local/share/GeoIP/GeoLite2-City.mmdb")
    ]
    
    for path in db_paths:
        if os.path.exists(path):
            return path
            
    # If not found, try to download
    return download_database(license_key)

def geolookup(ip_addr, license_key=None):
    """
    Look up geolocation information for an IP address using MaxMind's GeoIP2 database.
    Will attempt to download the database if not found.

    Args:
        ip_addr: The IP address to look up
        license_key: Optional MaxMind license key

    Returns:
        dict: A dictionary with geolocation information or error details.
             Always includes raw_output for debugging and custom parsing.
    """
    try:
        # Sanitize inputs
        ip_addr = ip_addr.strip() if ip_addr else ""
        license_key = license_key.strip() if license_key else None
        
        # Validate IP address format
        try:
            ip_obj = ipaddress.ip_address(ip_addr)
        except ValueError:
            return {
                "status": "error",
                "error": "Invalid IP address format",
                "query": {"ip": ip_addr}
            }

        # Check if IP is private
        if ip_obj.is_private:
            return {
                "status": "error",
                "error": "IP address not found in the database",
                "query": {"ip": ip_addr}
            }

        # Find or download the database
        db_path = find_or_download_database(license_key)
        if not db_path:
            if license_key:
                return {
                    "status": "error",
                    "error": "Invalid license key",
                    "query": {"ip": ip_addr}
                }
            else:
                return {
                    "status": "error",
                    "error": "GeoIP2 database not found and could not be downloaded. Please provide a valid MaxMind license key.",
                    "query": {"ip": ip_addr}
                }

        # Perform geolocation lookup
        with geoip2.database.Reader(db_path) as reader:
            response = reader.city(ip_addr)
            
            # Store raw output
            raw_output = {
                "continent": {
                    "code": response.continent.code,
                    "name": response.continent.name
                },
                "country": {
                    "iso_code": response.country.iso_code,
                    "name": response.country.name
                },
                "city": {
                    "name": response.city.name,
                    "confidence": response.city.confidence
                },
                "location": {
                    "latitude": response.location.latitude,
                    "longitude": response.location.longitude,
                    "accuracy_radius": response.location.accuracy_radius,
                    "time_zone": response.location.time_zone
                },
                "postal": {
                    "code": response.postal.code,
                    "confidence": response.postal.confidence
                },
                "subdivisions": [{
                    "iso_code": s.iso_code,
                    "name": s.name,
                    "confidence": s.confidence
                } for s in response.subdivisions],
                "traits": {
                    "autonomous_system_number": response.traits.autonomous_system_number,
                    "autonomous_system_organization": response.traits.autonomous_system_organization,
                    "ip_address": response.traits.ip_address,
                    "network": str(response.traits.network) if response.traits.network else None
                }
            }

            # Process the results with default "Unknown" for unmappable fields
            result = {
                "status": "success",
                "ip_addr": ip_addr,
                "country": "Unknown",
                "city": "Unknown",
                "region": "Unknown",
                "postal_code": "Unknown",
                "timezone": "Unknown",
                "latitude": None,
                "longitude": None,
                "asn": None,
                "as_org": "Unknown",
                "raw_output": raw_output
            }

            # Try to map known fields
            if response.country.name:
                result["country"] = response.country.name
                
            if response.city.name:
                result["city"] = response.city.name
                
            if response.subdivisions and response.subdivisions.most_specific.name:
                result["region"] = response.subdivisions.most_specific.name
                
            if response.postal.code:
                result["postal_code"] = response.postal.code
                
            if response.location.time_zone:
                result["timezone"] = response.location.time_zone
                
            if response.location.latitude is not None:
                result["latitude"] = float(response.location.latitude)
                
            if response.location.longitude is not None:
                result["longitude"] = float(response.location.longitude)
                
            if response.traits.autonomous_system_number:
                result["asn"] = response.traits.autonomous_system_number
                
            if response.traits.autonomous_system_organization:
                result["as_org"] = response.traits.autonomous_system_organization

            # Remove None values but keep "Unknown" strings
            result = {k: v for k, v in result.items() if v is not None}
            return result

    except geoip2.errors.AddressNotFoundError:
        return {
            "status": "error",
            "error": "IP address not found in the database",
            "query": {"ip": ip_addr}
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "error": "GeoIP2 database not found",
            "query": {"ip": ip_addr}
        }
    except geoip2.errors.InvalidRequestError:
        return {
            "status": "error",
            "error": "Invalid request",
            "query": {"ip": ip_addr}
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "query": {"ip": ip_addr}
        }

if __name__ == "__main__":
    print("Running geolookup as main")
    # Example usage
    result = geolookup("8.8.8.8")
    print(f"\nIPv4 Result: {result}")
    result = geolookup("2001:4860:4860::8888")
    print(f"\nIPv6 Result: {result}") 