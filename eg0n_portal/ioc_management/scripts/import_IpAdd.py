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

def import_ipadd_from_MISP():
    misp_url = "https://misp.bithorn.org"
    misp_key = ""

    # temporary extract last 100 IPs
    max_ioc = 100

    verify_cert = True
    timeout = 5

    if not verify_cert:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

    response.raise_for_status()
    attributes = response.json().get("response", {}).get("Attribute", [])

    # import IP addresses into the database
    for ip in attributes:
        try:
            IpAdd.objects.create(
                ip_address=ip['value'],
                description="Imported from MISP",
                author="MISP",
                lastchange_author="MISP",
            )
            print("IP Address %s created successfully.", ip['value'])
        except:
            print(f"Error creating IP address {ip['value']}. It may already exist.")

import_ipadd_from_MISP()
