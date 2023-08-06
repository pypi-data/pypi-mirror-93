import requests
from .dataclasses import Status


class Core:

    api = None

    def __init__(self, api):
        self.api = api


    def list(self):
        """
        Возвращает список объектов из Core
        """
        return self._response()


    def retrieve(self, lookup_field):
        """
        Возвращает один объект из Core
        """
        return self._response(lookup_field=lookup_field)


    def update(self, lookup_field, status, comment):
        """
        Обновляет значения полей Status и Comment сущности Event Core
        """

        if status not in [Status.ERROR, Status.SUCCESS, Status.FAILURE]:
            raise RuntimeError('Статус должен быть равен SCS, FAIL, ERROR')

        data = {
            'status': status,
            'comment': comment,
        }

        return self._response(data=data, lookup_field=lookup_field, method='put')


    def _get_url(self, lookup_field=None):
        if lookup_field:
            return self.api + str(lookup_field) + '/'
        else:
            return self.api

    def _response(self, data=None, lookup_field=None, method='get'):

        url = self._get_url(lookup_field=lookup_field)

        if method == 'put':
            response = requests.put(url, json=data)
        elif method == 'post':
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 500:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, 'Internal Server Error'))
        else:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, response.text[:255]))
