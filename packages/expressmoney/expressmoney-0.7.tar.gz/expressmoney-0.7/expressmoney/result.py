from dataclasses import dataclass


@dataclass
class Result:

    IN_PROCESS = 'INPR'  # Активное. требует изменения на: FAIL или SCS или HLD
    SUCCESS = 'SCS'  # Активное. блокирует создание нового события
    FAILURE = 'FAIL'  # Активное. блокирует создание нового события
    ERROR = 'ERROR'  # Не акитвное. Последнее событие завершилось ситемной ошибкой, бизнес-результат не известен

    status: str
    comment: any

    def __init__(self, status, comment=None):
        assert status in [
            self.IN_PROCESS,
            self.SUCCESS,
            self.FAILURE,
            self.ERROR,
        ], 'Wrong status'
        self.status = status
        self.comment = comment
