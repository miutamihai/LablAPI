import json


def get_max_probability(load):
    result_list = list(json.loads(load)['result'])
    res = result_list[0]['prediction']
    number_of_results = len(res)
    res = res[0]
    threshold = number_of_results == 3 and 0.5 or 0.75
    return res['probability'] > threshold and res['label'] or 'Unknown object'

