#!/usr/bin/env python

import requests
import json

url = 'http://api/switches'
resp = requests.get(url, verify=False)
data = json.loads(resp.text)
print(data.item)