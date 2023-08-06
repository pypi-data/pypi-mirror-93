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
