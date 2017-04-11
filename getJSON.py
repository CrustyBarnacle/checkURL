import json
from pprint import pprint
with open('URLcheckRSAexternal.json') as data_file:
    data = json.load(data_file)

print(data)

print(data['string'])
print(data['url'])
