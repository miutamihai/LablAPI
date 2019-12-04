import json


def get_max_probability(load):
    result_list = list(json.loads(load)['result'])
    res = result_list[0]['prediction'][0]
    return res['probability'] > 0.5 and res['label'] or 'Unknown object'

