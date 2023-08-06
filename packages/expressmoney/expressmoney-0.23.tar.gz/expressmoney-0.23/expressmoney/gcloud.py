import json
import base64
import requests
from google.cloud import pubsub_v1
from expressmoney.core import Core
from expressmoney.dataclasses import Status


class PubSub:
    """Взаимодействие с сервисов Google Cloud Pub/Sub"""

    project_id = None
    topic_name = None

    def __init__(self, project_id, topic_name):

        self.project_id = project_id
        self.topic_name = topic_name

    @staticmethod
    def extract_message(message):
        """
        Извлекает данные из message
        """
        message_bytes = base64.b64decode(message['data'])
        message = json.loads(message_bytes)
        return message['data']['message']

    def publish_messages(self, messages, key=None):
        """
        Публикует message в сервис Google Cloud Pub/Sub
        """

        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(self.project_id, self.topic_name)

        for message in messages:
            message_bytes = self._create_message_body(message=message, key=key)
            try:
                publish_future = publisher.publish(topic_path, data=message_bytes)
                publish_future.result()  # Verify the publish succeeded
            except Exception as e:
                print(e)
                raise Exception

    @staticmethod
    def _create_message_body(message, key=None):

        if key:
            message_json = json.dumps({
                'data': {'message': message.get(key)},
            })
        else:
            message_json = json.dumps({
                'data': {'message': message},
            })

        return message_json.encode('utf-8')


class Functions:
    """Взаимодействие Core c Cloud Functions"""

    def __init__(self, endpoint, api):

        self.core = Core(endpoint=endpoint)
        self.pubsub = PubSub(project_id='expressmoney', topic_name=endpoint)
        self.api = api

    def retrieve(self, data, headers=None):
        """Получение данных из стороннего сервиса с использованием REST API"""

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
        self._set_pk(self.pubsub.extract_message(message))

        # Получаю данные объекта Event по его pk
        self._set_event(self.core.retrieve(self.pk))

        # Обработка в зависимости от текущего статуса события
        if self.initial_event.get('status') == Status.NEW:

            # Обнвляю статус на IN_PROCESS
            self.core.update(lookup_field=self.pk, status=Status.IN_PROCESS,
                             comment='Sets status from NEW to IN_PROCESS')

            # Обрабатываю событие
            result = self._new()

            # Сохраняю результат
            self.core.update(lookup_field=self.pk, status=result.status, comment=result.comment)

        elif self.initial_event.get('status') == Status.IN_PROCESS:

            # Обрабатываю событие
            result = self._in_process()

            # Сохраняю результат
            self.core.update(lookup_field=self.pk, status=result.status, comment=result.comment)

        return Status.SUCCESS, 200

    def _set_pk(self, pk):
        """pk(primary key) для объекта Event"""
        self.pk = pk

    def _set_event(self, event):
        """Данные объекта Event"""
        self.initial_event = event

    def _new(self):
        """Подготовка доменных данных и передача их в сервиса _service_new()"""

        user = Core('user')
        profile = Core('profile')

        user_obj = user.retrieve(self.initial_event.get('user'))
        profile_obj = profile.retrieve(self.initial_event.get('user'))

        return self._service_new({**user_obj, **profile_obj})

    def _in_process(self):
        """Подготовка доменных данных и передача их в сервиса _service_in_process()"""

        return self._service_in_process()

    def _service_in_process(self):
        """Запускается для событий со статусом IN_PROCESS"""

        raise RuntimeError('Status IN_PROCESS недопустим для Event: {}'.format(str(data)))

    def _service_new(self, data):
        """Запускается для событий со статусом NEW"""

        return Status(Status.SUCCESS, str('Demo result comment in _service_new()')[255:])
