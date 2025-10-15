import os, sys
import requests, urllib3, time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eg0n_portal.settings")
import django
django.setup()

from ioc_management.models import IpAdd
from django.utils import timezone
from datetime import datetime, UTC

# import apiConfig model to get MISP API key
from core.models import apiConfig, BaseConfig as baseConfig

def import_ipadd_from_MISP():
    # get MISP API configuration from apiConfig model
    misp_url = apiConfig.objects.filter(api_name='MISP_bithorn').first().api_url
    misp_key = apiConfig.objects.filter(api_name='MISP_bithorn').first().api_key
    verify_cert = apiConfig.objects.filter(api_name='MISP_bithorn').first().api_verify_cert
    timeout = apiConfig.objects.filter(api_name='MISP_bithorn').first().api_timeout

    if not verify_cert:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # temporary extract last 100 IPs
    max_ioc = 100

    '''
    MISP test curl command:
    curl -X POST https://<MISP_URL>/attributes/restSearch -H "Authorization: <API_KEY>" -H "Accept: application/json" -H "Content-Type: application/json" -d '{ "returnFormat": "json", "limit": 0 }'
    MISP test curl command to get IPs:
    curl -X POST https://<MISP_URL>/attributes/restSearch -H "Authorization: <API_KEY>" -H "Accept: application/json" -H "Content-Type: application/json" -d '{ "controller": "attributes", "type": ["ip-src"], "to_ids": true, "deleted": false, "order": "timestamp desc", "limit": 100 }'
    '''

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

    # taxii server configuration
    taxii_url = apiConfig.objects.filter(api_name='taxii2_test').first().api_url
    taxii_username = baseConfig.objects.filter(param_name='taxii2_username').first().param_value
    taxii_password = baseConfig.objects.filter(param_name='taxii2_password').first().param_value
    taxii_apiroot = baseConfig.objects.filter(param_name='taxii2_apiroot').first().param_value
    taxii_collection_id = baseConfig.objects.filter(param_name='taxii2_collection_misp-ip').first().param_value

    # import IP addresses into the database
    for ip in attributes:

        # define misp url
        misp_event_url = f"{misp_url}/events/view/{ip['event_id']}"

        try:
            # add taxii indicator in cti-taxii format
            print(f"Preparing to send IP {ip['value']} to TAXII server...")
            taxii_data = {
                "objects": [
                    {
                        "type": "indicator",
                        "spec_version": "2.1",
                        "id": f"indicator--{ip['uuid']}",
                        "created": datetime.fromtimestamp(ip['timestamp'], UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "modified": datetime.fromtimestamp(ip['timestamp'], UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "name": f"MISP IP Address {ip['value']}",
                        "description": ip['comment'] if ip['comment'] else 'Imported from MISP',
                        "pattern": f"[ipv4-addr:value = '{ip['value']}']",
                        "pattern_type": "stix",
                        "valid_from": datetime.fromtimestamp(ip['timestamp'], UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
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
            #print(f"Preparing to send the following data to TAXII server:\n{taxii_data}\n")
            #print(f"Example cURL command: curl -u {taxii_username}:{taxii_password} -X POST {taxii_url}/{taxii_apiroot}/{taxii_collection_id}/objects/ -H 'Accept: application/taxii+json;version=2.1' -d '{taxii_data}'\n")

        except:
            print(f"Error...")

# main
if __name__ == "__main__":
    try:
        import_ipadd_from_MISP()
    except Exception as e:
        print(f"An error occurred: {e}")
