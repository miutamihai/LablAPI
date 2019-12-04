import requests


def get_prediction(image):
    url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'

    data = {'file': open(image, 'rb'), 'modelId': ('', 'a8496a92-9943-421b-974f-71ca05fad060')}
    try:
        response = requests.post(url, auth=requests.auth.HTTPBasicAuth('TH-BYEE3nlD8ooI1iL9Fc3dBJEZCEPFt', ''),
                                 files=data, timeout=15)
    except TimeoutError as ex:
        return 'Unknown object or service is down'

    return response.text
