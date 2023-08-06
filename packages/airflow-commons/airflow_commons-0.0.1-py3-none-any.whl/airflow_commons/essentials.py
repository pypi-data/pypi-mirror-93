import datetime as dt
from codecs import open as codec_open

import pytz

LEVELS = {1: 'ERROR', 2: 'WARN', 3: 'INFO'}


def LOGGER(message: str, level=3):
    """

    :param message:
    :param level:
    :return:
    """
    curr_time = dt.datetime.now(pytz.timezone("Europe/Moscow")).strftime('%Y-%m-%dT%H:%M:%S')
    print(LEVELS[level] + ' - [' + curr_time + '] -', message)


def read_sql(sql_file: str):
    """

    :param sql_file:
    :return:
    """
    with codec_open(sql_file, mode='r', encoding='utf-8-sig') as f:
        return f.read()
