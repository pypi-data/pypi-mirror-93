import requests
from expressmoney.core import Core
from expressmoney.gcloud import PubSub
from expressmoney.dataclasses import Status


class Service:
    """Взаимодействие сервисов с Core"""

    def __init__(self, endpoint, api):

        self.core = Core(endpoint=endpoint)
        self.pubsub = PubSub(project_id='expressmoney', topic_name=endpoint)
        self.api = api


    def retrieve(self, data, headers=None):
        """Получение данных из сервиса с использованием REST API"""

        try:
            response = requests.post(self.api, headers=headers, json=data, timeout=(30, 30))
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


    def update(self, message, context):
        """Для Event в статусе NEW вызывает _new для IN_PROCESS вызывает _in_process"""

        # Получаю pk(primary key) для объекта Event
        pk = self.pubsub.extract_message(message)

        # Получаю данные объекта Event по его pk
        event = self.core.retrieve(pk)

        # Обработка в зависимости от текущего статуса события
        if event.get('status') == Status.NEW:

            # Обнвляю статус на IN_PROCESS
            self.core.update(lookup_field=pk, status=Status.IN_PROCESS, comment='Sets status from NEW to IN_PROCESS')


            # Обрабатываю событие
            result = self._new(event)

            # Сохраняю результат
            self.core.update(lookup_field=pk, status=result.status, comment=result.comment)


        elif event.get('status') == Status.IN_PROCESS:

            # Обрабатываю событие
            result = self._in_process(event)

            # Сохраняю результат
            self.core.update(lookup_field=pk, status=result.status, comment=result.comment)


        return Status.SUCCESS, 200


    def _new(self, event):
        """Подготовка доменных данных и передача их в сервиса _service_new()"""

        user = Core('user')
        profile = Core('profile')

        user_obj = user.retrieve(event.get('user'))
        profile_obj = profile.retrieve(event.get('user'))

        return self._service_new({**user_obj, **profile_obj})


    def _in_process(self, event):
        """Подготовка доменных данных и передача их в сервиса _service_in_process()"""

        return self._service_in_process(event)


    def _service_in_process(self, data):
        """Запускается для событий со статусом IN_PROCESS"""

        raise RuntimeError('Status IN_PROCESS недопустим для Event: {}'.format(str(data)))


    def _service_new(self, data):
        """Запускается для событий со статусом NEW"""

        return Status(Status.SUCCESS, str('Demo result comment in _service_new()')[255:])
