import json


def get_headers():
    with open('headers.json') as json_file:
        data = json.load(json_file)
        return data


