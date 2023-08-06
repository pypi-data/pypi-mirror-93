from . import version

__version__ = version.get_current()


def get_default_retry_config():
    return {
        'max_retries': 10,
        'wait_uint': 6
    }
