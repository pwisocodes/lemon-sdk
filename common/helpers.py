from datetime import datetime


class Singleton(type):
    """ Metaclass Singleton
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def datetime_to_unixtimestamp(today: datetime, ddays: int, dhour: int, dmin: int):
    return (today.timedelta(days=ddays, hours=dhour, minutes=dmin)).strftime("%s")
