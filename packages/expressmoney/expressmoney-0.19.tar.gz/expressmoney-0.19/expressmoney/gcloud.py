import json
import base64
from google.cloud import pubsub_v1


class PubSub:
    """Взаимодействие с сервисов Google Cloud Pub/Sub"""

    project_id = None
    topic_name = None

    def __init__(self, project_id, topic_name):

        self.project_id = project_id
        self.topic_name = topic_name

    def extract_message(self, event):
        """
        Извлекает данные из message
        """
        message_bytes = base64.b64decode(event['data'])
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


    def _create_message_body(self, message, key=None):

        if key:
            message_json = json.dumps({
                'data': {'message': message.get(key)},
            })
        else:
            message_json = json.dumps({
                'data': {'message': message},
            })

        return message_json.encode('utf-8')
