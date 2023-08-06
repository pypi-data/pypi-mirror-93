import requests


def read_objects(api: str) -> dict:
    """
    Возвращает список объектов
    :param api: Ссылка на API Core
    :return: Список объектов
    """

    response = requests.get(api)

    if response.status_code == 200:
        objects = response.json()
        return objects
    elif response.status_code == 500:
        raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, 'Internal Server Error'))
    else:
        raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, response.text[:255]))


def read_object(api: str, object_pk: str) -> dict:
    """
    Возвращает один объект
    :param api: Ссылка на REST API
    :param object_pk: Идентификатор объекта
    :return: Объект
    """

    api = api + str(object_pk) + '/'

    response = requests.get(api)

    if response.status_code == 200:
        objects = response.json()
        return objects
    elif response.status_code == 500:
        raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, 'Internal Server Error'))
    else:
        raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, response.text[:255]))


def update_event(api_event: str, pk: str, status: str, comment: str) -> dict:
    """
    Обновляет значения полей Status и Comment сущности Event через API Core
    :param api_event: URL API Core
    :param pk: Идентификатор события
    :param status: Значение Status
    :param comment: Значение Comment
    :return: Обновленный Event
    """

    api_event = api_event + str(pk) + '/'

    data = {
        'status': status,
        'comment': comment,
    }

    response = requests.put(api_event, json=data)

    if response.status_code == 200:
        objects = response.json()
        return objects
    elif response.status_code == 500:
        raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, 'Internal Server Error'))
    else:
        raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, response.text[:255]))




def read_data(api: str, json: dict, headers=None) -> dict:
    """
    Запрос данных из сторорннего сервиса
    :param api: Ссылка на API Core
    :param headers: Заголовок для передачи в сторонний API
    :param json: Данные для передачи в сторонний API
    :return: Список объектов
    """

    response = requests.post(api, headers=headers, json=json)

    if response.status_code == 200:
        objects = response.json()
        return objects
    elif response.status_code == 500:
        raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, 'Internal Server Error'))
    else:
        raise RuntimeError('ERROR CORE: {} {}'.format(response.status_code, response.text[:255]))
