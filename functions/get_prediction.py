import requests


def get_prediction(image):
    url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'

    data = {'file': open(image, 'rb'), 'modelId': ('', 'b4e18a69-ddeb-4165-9f64-55b1ecc19446')}
    try:
        response = requests.post(url, auth=requests.auth.HTTPBasicAuth('TH-BYEE3nlD8ooI1iL9Fc3dBJEZCEPFt', ''),
                                 files=data, timeout=15)
    except TimeoutError as ex:
        return 'Unknown object or service is down'

    return response.text
