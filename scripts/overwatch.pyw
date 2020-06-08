import os
import sys
import time


def clean_cmd():
    os.system("del /q cmd\*")


def lock():
    with open('overwatch.lock', 'w') as fp:
        pass


def unlock():
    os.remove("overwatch.lock")


def cleanup():
    unlock()
    clean_cmd()
    os.system("taskkill /f /im chrome.exe")
    os.system("taskkill /f /im call.exe")


if __name__ == "__main__":
    clean_cmd()
    lock()
    while True:
        if(os.path.exists("cmd/call.start")):
            clean_cmd()
            os.system("/scripts/run.bat")
        if(os.path.exists("cmd/cleanup.chrome")):
            clean_cmd()
            os.system("taskkill /f /FI \"WINDOWTITLE eq VIEWER\"")
            os.system("taskkill /f /im chrome.exe")
        if(os.path.exists("cmd/cleanup.all")):
            cleanup()
            sys.exit(0)
        time.sleep(1)
