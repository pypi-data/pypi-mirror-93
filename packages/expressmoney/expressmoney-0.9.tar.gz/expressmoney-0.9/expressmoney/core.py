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


    def retrieve(self, pk):
        """
        Возвращает один объект из Core
        """
        return self._response(pk=pk)


    def update(self, pk, status, comment):
        """
        Обновляет значения полей Status и Comment сущности Event Core
        """

        if status not in [Status.ERROR, Status.SUCCESS, Status.FAILURE]:
            raise RuntimeError('Статус должен быть равен SCS, FAIL, ERROR')

        data = {
            'status': status,
            'comment': comment,
        }

        return self._response(data=data, pk=pk, get=False)


    def _get_url(self, pk=None):
        if pk:
            return self.api + str(pk) + '/'
        else:
            return self.api

    def _response(self, data=None, pk=None, get=True):

        url = self._get_url(pk=pk)

        if get:
            response = requests.get(url)
        else:
            response = requests.put(url, json=data)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 500:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, 'Internal Server Error'))
        else:
            raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, response.text[:255]))
