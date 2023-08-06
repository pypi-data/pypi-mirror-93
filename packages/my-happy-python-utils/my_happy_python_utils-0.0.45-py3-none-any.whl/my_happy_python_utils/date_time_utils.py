import datetime

from . import version

__version__ = version.get_current()


def now_str():
    return f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f}"


def now_str_for_file_name():
    return f"{datetime.datetime.now():%Y_%m_%d_%H_%M_%S_%f}"


def timestamp_to_str(timestamp):
    return f"{datetime.datetime.fromtimestamp(timestamp):%Y-%m-%d %H:%M:%S.%f}"


def timestamp_to_str_second(timestamp):
    return f"{datetime.datetime.fromtimestamp(timestamp):%Y-%m-%d %H:%M:%S}"


def chage_datetime_fromat(opt={}):
    my_date_time = datetime.datetime.strptime(
                        opt['date_time'],
                        opt['from_format'])

    return my_date_time.strftime(opt.get('to_format', '%Y-%m-%d %H:%M:%S'))
