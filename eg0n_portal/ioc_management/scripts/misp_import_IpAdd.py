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
from datetime import datetime

# import apiConfig model to get MISP API key
from core.models import apiConfig

def import_ipadd_from_MISP():
    # get MISP API configuration from apiConfig model
    misp_url = apiConfig.objects.filter(api_name='MISP_bithorn').first().api_url
    misp_key = apiConfig.objects.filter(api_name='MISP_bithorn').first().api_key
    verify_cert = 'True'
    timeout = apiConfig.objects.filter(api_name='MISP_bithorn').first().timeout

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

    data = {
        "controller": "attributes",
        "type": ["ip-src"],
        "to_ids": True,
        "deleted": False,
        "order": "timestamp desc",
        "limit": max_ioc
    }

    headers = {
        "Authorization": misp_key,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }   

    response = requests.post(
        f"{misp_url}/attributes/restSearch",
        json=data,
        headers=headers,
        verify=verify_cert,
        timeout=timeout
    )

    response.raise_for_status() # will raise an error for bad responses
    attributes = response.json().get("response", {}).get("Attribute", [])

    # import IP addresses into the database
    for ip in attributes:
        try:
            IpAdd.objects.create(
                ip_address=ip['value'],
                description=ip['comment'] if ip['comment'] else 'Imported from MISP',
                author="MISP",
                lastchange_author="MISP",
            )
            print("IP Address %s created successfully.", ip['value'])
        except:
            print(f"Error creating IP address {ip['value']}. It may already exist.")

# main
if __name__ == "__main__":
    try:
        import_ipadd_from_MISP()
    except Exception as e:
        print(f"An error occurred: {e}")
