import os, sys, inspect
import subprocess


from . import version

__version__ = version.get_current()

mapbox_access_token = 'pk.eyJ1IjoiZ2dzZXJ2aWNlMDA3IiwiYSI6ImNqcmxvYWp5YjBhbm40NHQycnQ0eGx5amEifQ._OQnUSuagFjTSCFWmThDOw'

def exportMapboxToken():
    commands = """
        export MAPBOX_API_KEY={token}
        export MAPBOX_ACCESS_TOKEN={token}
    """.format(token=mapbox_access_token).strip()

    os.environ["MAPBOX_API_KEY"] = mapbox_access_token
    os.environ["MAPBOX_ACCESS_TOKEN"] = mapbox_access_token

    return runCommands(commands)

def runCommands(commands):
    process = subprocess.Popen(
                            commands,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)

    stdout, stderr = process.communicate()

    if len(stdout) > 0:
        stdout = stdout.decode('utf-8')

    if len(stderr) > 0:
        stderr = stderr.decode('utf-8')

    return (stdout, stderr)
