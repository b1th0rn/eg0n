#!/usr/bin/env python3

import requests

token="6e32cc14333300490f42a7d472ac9b27719b6aee"
header = {
    "Authorization": f"Token {token}"
}
url = "http://localhost:9000/api/user/"

# for i in range(1, 200):
#     payload = {
#         "username": f"test-user-{i}"
#     }
#     res = requests.post(url, headers=header, json=payload)
#     res.raise_for_status()

for i in range(1, 4):
    payload = {
        "username": f"test-user-{i}"
    }
    res = requests.post(url, headers=header, json=payload)
    res.raise_for_status()
