import pyaudio
import wave
import sys
import os
import asyncio
import time
import atexit
import re
import numpy as np
from numpy import array
from aubio import pitch
from ast import literal_eval
from multiprocessing import Process
from datetime import datetime
from colorama import init, Fore, Back, Style
init()

with open('cmd/call.starting', 'w') as f:
    pass

log_file = open("logs/call.log", "a")


def log(string):
    sure = str(string)
    sure = re.sub('(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', '', sure)
    log_file.write(sure)
    log_file.write("\n")
    log_file.flush()
    print(string + Style.RESET_ALL)


def cls(): return os.system('cls')


defaultframes = 512

# Pitch
tolerance = 0.8
downsample = 1
win_s = 4096 // downsample  # fft size
hop_s = 512 // downsample  # hop size
pitch_o = pitch("yin", win_s, hop_s, 48000)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)


recorded_frames = []
device_info = {}
useloopback = False
recordtime = 1

# Use module
p = pyaudio.PyAudio()

# Set default to first in list or ask Windows
try:
    default_device_index = p.get_default_input_device_info()
except IOError:
    default_device_index = -1

# Select Device
#log( "Available devices:\n")
for i in range(0, p.get_device_count()):
    info = p.get_device_info_by_index(i)
    # log( str(info["index"]) +  ": \t %s \n \t %s \n" % (
    # info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))

    if default_device_index == -1:
        default_device_index = info["index"]

# Handle no devices available
if default_device_index == -1:
    log("No device available. Quitting.")
    exit()


# Get input or default
device_id = 4  # int(input("Choose device [" +  str(
# default_device_index) +  "]: ") or default_device_index)
log("")

# Get device info
try:
    device_info = p.get_device_info_by_index(device_id)
except IOError:
    device_info = p.get_device_info_by_index(default_device_index)
    log(
        "Selection not available, using default.")

# Choose between loopback or standard mode
is_input = device_info["maxInputChannels"] > 0
is_wasapi = (p.get_host_api_info_by_index(
    device_info["hostApi"])["name"]).find("WASAPI") != -1
if is_input:
    log("Selection is input using standard mode.\n")
else:
    if is_wasapi:
        useloopback = True
        log(
            "Selection is output. Using loopback mode.\n")
    else:
        log(
            "Selection is output and does not support loopback mode. Quitting.\n")
        exit()

recordtime = 0  # int(input("Record time in seconds [" +  str(
# recordtime) +  "]: ") or recordtime)
# Open stream
channelcount = 1  # device_info["maxInputChannels"] if (
# device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]


# Start Recording
# exit()
buzzes = 0
last_pitch = 0
last_pitch_match = 0
hang_up = False
alerts = 0
since_last_alert = 0
listening_time = 0
start = int(datetime.now().timestamp())
is_listening = False
# for i in range(0, int(int(device_info["defaultSampleRate"]) / defaultframes * recordtime)):
stream = p.open(format=pyaudio.paFloat32,
                channels=channelcount,
                rate=int(device_info["defaultSampleRate"]),
                input=True,
                frames_per_buffer=defaultframes,
                input_device_index=device_info["index"],
                as_loopback=useloopback)
delay_start = 5

cur_phone_number = 0
numbers = []
first_call = True
reading = False


def get_phone_number():
    global cur_phone_number
    global numbers
    numbers = []
    output = ""
    with open('phonenumbers', 'r') as f:
        output = f.read()
    lines = output.split("\n")
    for line in lines:
        if(line.startswith("#") is False and line.strip() and line not in ['\n', '\r\n']):
            numbers.append(line.split(" ")[0])
    length = numbers.__len__()
    if(cur_phone_number > length - 1):
        cur_phone_number = 0
    number = numbers[cur_phone_number]
    if(length > 1):
        cur_phone_number = cur_phone_number + 1
    return number


phonenumber = ""


def start_new_call():
    global last_pitch_match
    global since_last_alert
    global listening_time
    global alerts
    global start
    global is_listening
    global first_call
    global phonenumber
    if(os.path.exists("cmd/call.calling")):
        os.remove("cmd/call.calling")
    alerts = 0
    is_listening = False
    last_pitch_match = 0
    since_last_alert = 0
    r_delay = round((np.random.rand(1)[0] * 4) + 1, 3)
    if(first_call):
        r_delay = 0
    log("Delaying for {} seconds...".format(r_delay))
    check_exit()
    os.system('/ahk/hangup.ahk')
    time.sleep(r_delay)
    if(first_call is not False):
        first_call = False
    output = get_phone_number()
    phonenumber = output
    log(Fore.CYAN + "New Call to " + output)
    os.system('/ahk/caller.ahk ' + output)
    with open('cmd/call.calling', 'w') as f:
        f.write(output)
        pass
    listening_time = 0
    time.sleep(3)
    start = int(datetime.now().timestamp())
    log(Fore.YELLOW + "Awaiting Audio")


def busy_tone(buzzes=0):
    log(Fore.RED + "HANG UP | Buzzes: " + str(buzzes))
    with open('cmd/call.hungup', 'w') as f:
        f.write(phonenumber)
        pass
    check_exit()
    start_new_call()


def read():
    global alerts
    global reading
    global last_pitch_match
    global since_last_alert
    global listening_time
    global start
    global is_listening
    global buzzes
    global phonenumber
    # log("Listening")
    # sys.stdout.flush()
    buffer = stream.read(defaultframes)
    if(is_listening is not True):
        log(Fore.YELLOW + "Listening...")
        is_listening = True
    listening_time = listening_time + 1
    if(int(datetime.now().timestamp()) - start > 15):
        log(Fore.GREEN + "CALL CONNECTED")
        with open("cmd/call.connected", "w") as f:
            f.write(phonenumber)
        check_exit()
        # start_new_call()
        exit()
    frame = np.frombuffer(buffer, dtype=np.float32)
    pitch = pitch_o(frame)[0]
    if(round(pitch, 1) < 67 and round(pitch, 1) > 63):
        buzzes = buzzes + 1
    if(pitch < 30):
        if(buzzes > 25):
            busy_tone(buzzes)
        buzzes = 0
    sys.stdout.flush()
    reading = False


def check_input():
    lines = sys.stdin.readlines()
    for line in lines:
        if(line == "exit"):
            exit()


def close_viewer():
    os.system("taskkill /f /FI \"WINDOWTITLE eq VIEWER\"")


def check_exit():
    if(os.path.exists("cmd/exit.now")):
        os.remove("cmd/exit.now")
        log("Exit File Found - Now")
        close_viewer()
        exit()
    if(os.path.exists("cmd/exit.hangup")):
        os.remove("cmd/exit.hangup")
        log("Exit File Found - Hang Up")
        close_viewer()
        os.system("/ahk/hangup.ahk")
        exit()


def cleanup():
    log("End ------------------------------------------------------------------")
    # Stop Recording
    stream.stop_stream()
    stream.close()
    log_file.close()
    # Close module
    p.terminate()
    if(os.path.exists("cmd/call.calling")):
        os.remove("cmd/call.calling")
    if(os.path.exists("cmd/call.running")):
        os.remove("cmd/call.running")


atexit.register(cleanup)

cls()
log("Initializing...")
log("You have {} seconds to leave the VM with your mouse".format(delay_start))
for i in range(0, delay_start):
    log("Waiting... {}".format(5 - i))
    time.sleep(1)
cls()
log("Setting Volume...")
os.system("includes\setvol.exe unmute")
os.system("includes\setvol.exe 75")
os.system("/ahk/prep.ahk")
#os.system("cmd/call includes\windowMode -title \"CALLER\" -mode restore")
log("Opening Chrome...")
os.system("start chrome https://hangouts.google.com --window-size=512,512 --window-position=10,10")
time.sleep(5)
log("Resizing Windows...")
os.system('/ahk/resize.ahk')
log("Opening Viewer...")
sys.stdout.flush()
os.system('/ahk/down.ahk')
os.system("start \"VIEWER\" python scripts/listen.py")
os.system('/ahk/up.ahk')
time.sleep(2)

log("Starting...")
log("Sample Rate: " + str(int(device_info["defaultSampleRate"])))
sys.stdout.flush()


def main():
    global reading
    os.remove('cmd/call.starting')
    with open('cmd/call.running', 'w') as f:
        pass
    start_new_call()
    while True:
        check_exit()
        if(reading):
            check_input()
        else:
            reading = True

            read()


if __name__ == "__main__":
    main()
