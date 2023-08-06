import requests


class Service:

    url = None

    def __init__(self, url):
        self.url = url


    def retrieve(self, data, headers=None):


        try:
            response = requests.post(self.url, headers=headers, json=data, timeout=(30, 30))
        except requests.exceptions.ConnectTimeout as error:
            raise error
        except requests.exceptions.ReadTimeout as error:
            raise error
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 500:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, 'Internal Server Error'))
        else:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, response.text[:255]))
