##########################################################################
# Script to import IP addresses from MISP and send to TAXII2 server (cti-taxii-server)
# Usage: python misp_to_taxii2.py
# Requires: requests, urllib3
##########################################################################

import requests, urllib3, time, traceback
from datetime import datetime, UTC

# misp configuration
misp_url = "https://misp.example.com"
misp_key = "YOUR_MISP_API_KEY"
verify_cert = False
timeout = 30
max_ioc = 100
# taxii configuration
taxii_url = "https://taxii.example.com"
taxii_username = "YOUR_TAXII_USERNAME"
taxii_password = "YOUR_TAXII_PASSWORD"
taxii_apiroot = "api-root"
taxii_collection_id = "collection-id-for-misp-ips"  

# function to import IP addresses from MISP and send to TAXII2 server
def import_ipadd_from_MISP():

    if not verify_cert:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # misp_data to get IP addresses
    misp_data = {
        "controller": "attributes",
        "type": ["ip-src"],
        "to_ids": True,
        "deleted": False,
        "order": "timestamp desc",
        "limit": max_ioc
    }

    misp_headers = {
        "Authorization": misp_key,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }   

    response = requests.post(
        f"{misp_url}/attributes/restSearch",
        json=misp_data,
        headers=misp_headers,
        verify=verify_cert,
        timeout=timeout
    )

    response.raise_for_status() # will raise an error for bad responses
    attributes = response.json().get("response", {}).get("Attribute", [])

    # import IP addresses into the database
    for ip in attributes:

        # define misp url
        misp_event_url = f"{misp_url}/events/view/{ip['event_id']}"

        try:
            # add taxii indicator in cti-taxii format
            taxii_data = {
                "objects": [
                    {
                        "type": "indicator",
                        "spec_version": "2.1",
                        "id": f"indicator--{ip['uuid']}",
                        "created": datetime.fromtimestamp(int(ip['timestamp']), UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "modified": datetime.fromtimestamp(int(ip['timestamp']), UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "name": f"MISP IP Address {ip['value']}",
                        "description": ip['comment'] if ip['comment'] else 'Imported from MISP',
                        "pattern": f"[ipv4-addr:value = \'{ip['value']}\']",
                        "pattern_type": "stix",
                        "valid_from": datetime.fromtimestamp(int(ip['timestamp']), UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "external_references": [
                            {
                                "source_name": "MISP",
                                "description": f"MISP Event {ip['event_id']}",
                                "url": misp_event_url,
                                "external_id": str(ip['event_id'])
                            }
                        ]
                    }
                ]
            }

            # test print taxii_data
            print(f"Preparing to send the following data to TAXII server:\n{taxii_data}\n")
            print(f"Example cURL command: curl -u {taxii_username}:{taxii_password} -X POST {taxii_url}/{taxii_apiroot}/collections/{taxii_collection_id}/objects/ -H 'Accept: application/taxii+json;version=2.1' -d \"{taxii_data}\"\n")

            # http request to taxii server
            taxii_response = requests.post(
                f"{taxii_url}/{taxii_apiroot}/collections/{taxii_collection_id}/objects/",
                json=taxii_data,
                auth=(taxii_username, taxii_password),
                headers={
                    # media type for TAXII 2.1
                    "Accept": "application/taxii+json;version=2.1",
                    "Content-Type": "application/taxii+json;version=2.1"
                },
                verify=True,
                timeout=30
            )
            taxii_response.raise_for_status() # will raise an error for bad responses
            print(f"Successfully sent IP {ip['value']} to TAXII server. Response status code: {taxii_response.status_code}\n")
            time.sleep(1) # to avoid overwhelming the server

        except Exception as e:
            print(f"Error... {e}")
            # traceback.print_exc()

# main
if __name__ == "__main__":
    try:
        import_ipadd_from_MISP()
    except Exception as e:
        print(f"An error occurred: {e}")
