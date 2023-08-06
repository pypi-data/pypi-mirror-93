from . import version

__version__ = version.get_current()


def get_default_splitter():
    return '^^'
