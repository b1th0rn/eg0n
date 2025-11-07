#!/usr/bin/env python3

import requests
import sys


# from django.contrib.auth.models import Group, User

token="7d0357c974b6f6bce5fb4bd37a74b640d1e19399" # admin
header = {
    "Authorization": f"Token {token}"
}
url = f"http://localhost:9000/api/user/"

res = requests.post(url, headers=header, json={"username": "ciao", "first_name": "ciao"})
print(res.status_code)
print(res.text)

sys.exit()

# Admin
token="7d0357c974b6f6bce5fb4bd37a74b640d1e19399"
header = {
    "Authorization": f"Token {token}"
}

url = "http://localhost:9000/api/user/206/"
payload = {
    "is_staff": True,
    "is_superadmin": False,
    "groups":[],
}
res = requests.patch(url, json=payload, headers=header)
print("#" * 70)
print("# BEFORE")
print("#" * 70)
print(res.json())
print("#" * 70)

# Staff
token="e34ad91624c425b6b794e3cb242363c3fd3532e1"
header = {
    "Authorization": f"Token {token}"
}

url = "http://localhost:9000/api/user/206/"
payload = {
    "groups": [1],
}
res = requests.patch(url, headers=header, json=payload)

print(res.status_code, res.text)

res = requests.get(url, headers=header)
print("#" * 70)
print("# AFTER")
print("#" * 70)
print(res.json())
print("#" * 70)
