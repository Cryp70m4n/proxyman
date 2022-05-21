import requests
import json

resp = requests.get("http://127.0.0.1:4334/api/show_sources")
print(resp.json())
