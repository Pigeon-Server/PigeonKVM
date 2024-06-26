#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import signal
import time

from util.logger import Log
import app.apps

stop = False


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipkvm.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def stopSignal(signum, frame):
    global stop
    print(signum)
    print(frame)
    if stop is not True:
        Log.success("应用程序正在停止......")
        stop = True
        app.apps.cameraObj.stopCamera()
        time.sleep(3)
        os._exit(0)
    return signum


if __name__ == '__main__':
    Log.info("应用程序启动中......")
    signal.signal(signal.SIGINT, stopSignal)
    main()
