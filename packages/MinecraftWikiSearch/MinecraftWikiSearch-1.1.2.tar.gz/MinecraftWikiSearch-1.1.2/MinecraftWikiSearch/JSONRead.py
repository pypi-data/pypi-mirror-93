import json
import os

if os.path.exists('config.json'):
    file = open('config.json', 'r')
    content = file.read()
else:
    Config = {
        "FasterLoad": True,
        "EasyInput": False,
        "EasyReturn": False
    }
    with open('config.json', 'w') as f:
        json.dump(Config, f)
    file = open('config.json', 'r')
    content = file.read()

Dict = json.loads(content)
EasyInput = Dict["EasyInput"]
EasyReturn = Dict["EasyReturn"]
FastLoad = Dict["FasterLoad"]
file.close()