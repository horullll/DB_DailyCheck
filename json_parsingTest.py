import json

with open('instance_list.json') as instance_list:
    json_data = json.load(instance_list)

    print(json_data);