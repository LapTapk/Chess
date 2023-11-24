import json

with open('jsons/images.json') as f:
    data_json = f.read()
    data = json.loads(data_json)
    print(data)