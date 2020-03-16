import json

def getInstanceList() :
    with open('instance_list.json') as instance_list:
        json_data = json.load(instance_list)
        instance_list = list(json_data.keys())
    return instance_list
