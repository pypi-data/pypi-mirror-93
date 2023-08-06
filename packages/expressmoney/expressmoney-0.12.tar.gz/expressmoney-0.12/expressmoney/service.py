import requests


class Service:

    api = None

    def __init__(self, api):
        self.api = api

    def list(self):
        """
        Возвращает список объектов из Core
        """
        return self._response()



    def _response(self, data=None, pk=None, headers=None, get=True):

        url = self._get_url(pk=pk)

        if get:
            response = requests.get(url, headers=headers)
        else:
            response = requests.put(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 500:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, 'Internal Server Error'))
        else:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, response.text[:255]))


    def _get_url(self, pk=None):
        if pk:
            return self.api + str(pk) + '/'
        else:
            return self.api
