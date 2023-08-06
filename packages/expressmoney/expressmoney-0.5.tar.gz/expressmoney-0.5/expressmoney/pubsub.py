import json
import base64
from google.cloud import pubsub_v1


def publish_message(objects: list, project_id: str, topic_name: str) -> bool:
    """
    Публикует сообщения в сервис Google Cloud Pub/Sub
    :param objects: Список обьектов полученный из API Core
    :param project_id: Идентификатор проекта в Google Cloud Platform
    :param topic_name: Название Темы из сервиса Google Cloud Pub/Sub
    :return: Результат отправки
    """

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    for obj in objects:
        message_json = json.dumps({
            'data': {'message': obj.get('pk')},
        })
        message_bytes = message_json.encode('utf-8')

        try:
            publish_future = publisher.publish(topic_path, data=message_bytes)
            publish_future.result()  # Verify the publish succeeded
        except Exception as e:
            print(e)
            raise Exception

    return True


def read_pk(event) -> int:
    """
    Извлекает pk из сообщения Google Cloud Pub/Sub
    :param event: Сообщения Google Cloud Pub/Sub
    :return: Идентификатор обьекта API Core
    """
    message_bytes = base64.b64decode(event['data'])
    message = json.loads(message_bytes)
    pk = int(message['data']['message'])
    return pk
