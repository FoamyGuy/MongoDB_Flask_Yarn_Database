import requests
import random

url = "http://localhost:5000/yarn"



resp = requests.post(url, json={
    "color": 0xff00ff,
    "amount": "3 skeins",
    "notes": "Super Fluffy pink"
})

print(f"{resp.status_code}")