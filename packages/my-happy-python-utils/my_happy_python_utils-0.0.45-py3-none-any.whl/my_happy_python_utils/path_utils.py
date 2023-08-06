import os, sys, inspect
import subprocess


from . import version

__version__ = version.get_current()


def get_current_dir_for_jupyter():
    """Get the current path for jupyter"""
    return getCurrentDir(os.getcwd())


def get_current_dir(current_file):
    """Get the current path"""
    current_dir = os.path.dirname(current_file)

    return current_dir


def get_parent_dir(current_file):
    """Get the parth path"""
    current_dir = os.path.dirname(current_file)
    parent_dir = os.path.dirname(current_dir)

    return parent_dir


def join(path, *paths):
    """Path join"""
    return os.path.join(path, *paths)


def insert_parent_package_dir(current_file):
    """Insert parent package dir"""
    current_dir = os.path.dirname(current_file)
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
