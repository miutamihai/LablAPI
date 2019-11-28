import json


def get_max_probability(load):
    result_list = list(json.loads(load)['result'])
    res = None
    for pair in result_list[0]['prediction']:
        if res is None:
            res = pair
        elif pair['probability'] > res['probability']:
            res = pair
    return res['label']

