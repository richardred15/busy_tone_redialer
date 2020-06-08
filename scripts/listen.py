import pyaudio
import wave
import sys
import os
import asyncio
import time
import atexit
import numpy as np
from numpy import array
from aubio import pitch
from ast import literal_eval
from multiprocessing import Process
from datetime import datetime


def cls(): return os.system('cls')


cls()
print("Initializing...")


defaultframes = 512

# Pitch
tolerance = 0.8
downsample = 1
win_s = 4096 // downsample  # fft size
hop_s = 512 // downsample  # hop size
pitch_o = pitch("yin", win_s, hop_s, 48000)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)


class textcolors:
    blue = '\033[94m'
    green = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    end = '\033[0m'


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
#print( "Available devices:\n")
for i in range(0, p.get_device_count()):
    info = p.get_device_info_by_index(i)
    # print( str(info["index"]) +  ": \t %s \n \t %s \n" % (
    # info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))

    if default_device_index == -1:
        default_device_index = info["index"]

# Handle no devices available
if default_device_index == -1:
    print("No device available. Quitting.")
    exit()


# Get input or default
device_id = 4  # int(input("Choose device [" +  str(
# default_device_index) +  "]: ") or default_device_index)
print("")

# Get device info
try:
    device_info = p.get_device_info_by_index(device_id)
except IOError:
    device_info = p.get_device_info_by_index(default_device_index)
    print(
        "Selection not available, using default.")

# Choose between loopback or standard mode
is_input = device_info["maxInputChannels"] > 0
is_wasapi = (p.get_host_api_info_by_index(
    device_info["hostApi"])["name"]).find("WASAPI") != -1
if is_input:
    print("Selection is input using standard mode.\n")
else:
    if is_wasapi:
        useloopback = True
        print(
            "Selection is output. Using loopback mode.\n")
    else:
        print(
            "Selection is output and does not support loopback mode. Quitting.\n")
        exit()
channelcount = 1  # device_info["maxInputChannels"] if (

# for i in range(0, int(int(device_info["defaultSampleRate"]) / defaultframes * recordtime)):
stream = p.open(format=pyaudio.paFloat32,
                channels=channelcount,
                rate=int(device_info["defaultSampleRate"]),
                input=True,
                frames_per_buffer=defaultframes,
                input_device_index=device_info["index"],
                as_loopback=useloopback)

buzzes = 0


def read():
    global buzzes
    buffer = stream.read(defaultframes)

    frame = np.frombuffer(buffer, dtype=np.float32)
    pitch = pitch_o(frame)[0]
    print(" |=" + ("=" * int(pitch / 5)))
    if(round(pitch, 1) < 67 and round(pitch, 1) > 63):
        buzzes = buzzes + 1
    if(pitch < 30):

        buzzes = 0


while True:
    read()
