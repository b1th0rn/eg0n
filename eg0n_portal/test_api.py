#!/usr/bin/env python3

import requests
import sys
import random


# from django.contrib.auth.models import Group, User

# token="7d0357c974b6f6bce5fb4bd37a74b640d1e19399" # admin
# header = {
#     "Authorization": f"Token {token}"
# }
# url = f"http://localhost:9000/api/user/"

# res = requests.post(url, headers=header, json={"username": "ciao", "first_name": "ciao"})
# print(res.status_code)
# print(res.text)

# sys.exit()

# # Admin
# token="7d0357c974b6f6bce5fb4bd37a74b640d1e19399"
# header = {
#     "Authorization": f"Token {token}"
# }

# url = "http://localhost:9000/api/user/206/"
# payload = {
#     "is_staff": True,
#     "is_superadmin": False,
#     "groups":[],
# }
# res = requests.patch(url, json=payload, headers=header)
# print("#" * 70)
# print("# BEFORE")
# print("#" * 70)
# print(res.json())
# print("#" * 70)

# Staff
# token="5b4600a3a09456b1f0716a3be753bb3d41ab7bd8"
# header = {
#     "Authorization": f"Token {token}"
# }

# url = "http://localhost:9000/api/group/"
# payload = {
#     "name": f"test{random.randint(100, 1000)}",
# }
# res = requests.post(url, headers=header, json=payload)

# print(res.status_code, res.text)



res = requests.post("http://localhost:9000/token/create")
print(res.status_code)