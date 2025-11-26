"""
Simple VirusTotal Sample Download Tool
Downloads malware samples from VirusTotal using SHA256 hash
"""
import os
import re
import requests
import argparse
from datetime import datetime

def is_valid_sha256(hash_string: str) -> bool:
    """Validate if the string is a valid SHA256 hash"""
    return bool(re.match(r'^[A-Fa-f0-9]{64}$', hash_string))

def download_sample(api_key: str, sha256_hash: str, output_file: str, debug: bool = False):
    """
    Download a specific sample by SHA256 hash from VirusTotal
    """
    # API endpoint
    url = "https://virustotal.com/api/v3/files/{}/download".format(sha256_hash)
    
    # Headers
    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }

    try:
        print("Requesting download for: {}".format(sha256_hash))
        
        if debug:
            print("URL: {}".format(url))
            print("Headers:", headers)

        # Make the request
        response = requests.get(url, headers=headers, stream=True)

        # Check for errors
        if response.status_code != 200:
            error_msg = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            #print(f"Error ({response.status_code}): {error_msg}")
            return False

        # Save the file
        #print(f"Downloading to {output_file}...")
        with open(output_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        #print(f"Successfully downloaded to {output_file}")
        return True

    except Exception as e:
        #print(f"Download error: {str(e)}")
        if debug:
            import traceback
            traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Download malware samples from VirusTotal using SHA256 hash"
    )
    parser.add_argument("-s", "--sha256", required=True, 
                        help="SHA256 hash to download")
    parser.add_argument("-o", "--output", required=True, 
                        help="Output file name")
    parser.add_argument("-k", "--apikey", 
                        help="VirusTotal API Key", 
                        default=os.getenv("VT_API_KEY"))
    parser.add_argument("-d", "--debug", 
                        help="Enable debug output", 
                        action="store_true")

    args = parser.parse_args()

    if not args.apikey:
        print("Error: VirusTotal API key required. Provide it as argument (-k) or set VT_API_KEY environment variable.")
        return

    # Validate SHA256 hash
    if not is_valid_sha256(args.sha256):
        #print(f"Error: '{args.sha256}' is not a valid SHA256 hash")
        return

    if args.debug:
        print("Debug mode enabled")

    # Download the sample
    download_sample(args.apikey, args.sha256.lower(), args.output, args.debug)

if __name__ == "__main__":
    main()