import json


def serializer_data(data):
    json_string = json.dumps(data)
    return json_string

