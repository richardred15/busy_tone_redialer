from tkinter import *
import tkinter.font as font
from datetime import datetime
from playsound import playsound
import os


def write_file(name):
    with open(name, 'w') as f:
        pass


def start_caller():
    write_file("cmd/call.start")


def exit_caller_now():
    write_file("cmd/exit.now")


def exit_chrome():
    write_file("cmd/cleanup.chrome")


def exit_cleanup():
    exit_caller_now()
    exit_chrome()


def exit_all():
    exit_caller_now()
    write_file("cmd/cleanup.all")


in_call = False


def check_overwatch_status():
    global in_call
    if(os.path.exists("overwatch.lock")):
        runningText.set("OverWatch Running")

        if(os.path.exists("cmd/call.calling")):
            with open("cmd/call.calling", "r") as text:
                callingText.set("Currently Calling...\n"+text.read())
        else:
            callingText.set("Delay...")
        if(os.path.exists("cmd/call.running")):
            callerRunningText.set("Caller Running...")
        else:
            callerRunningText.set("Caller Disabled...")
            callingText.set("")
        if(os.path.exists("cmd/call.starting")):
            callerRunningText.set("Caller Starting...")
        if(os.path.exists("cmd/call.connected")):
            callingText.set("In Call...")
            if(in_call is False):
                with open("cmd/call.connected", "r") as text:
                    outcomeText.set("Last Call Connected\n" + text.read())
                playsound("media/TADA.WAV")
                in_call = True
        else:
            in_call = False
        if(os.path.exists("cmd/call.hungup")):
            with open("cmd/call.hungup", "r") as text:
                outcomeText.set("Last Call Hung Up\n" + text.read())
            os.remove("cmd/call.hungup")
    else:
        runningText.set("OverWatch Disabled")
        outcomeText.set("")
        callingText.set("")
        callerRunningText.set("")

    master.after(1000, check_overwatch_status)


firstLoad = True
master = Tk()
master.minsize(352, 296)

bigFont = font.Font(family='Segoe UI', size=24)
listFont = font.Font(family='Segoe UI', size=18)
chatFont = font.Font(family='Segoe UI', size=16)
infoFont = font.Font(family='Segoe UI', size=12)
stampFont = font.Font(family='Segoe UI', size=12)


runningText = StringVar()
outcomeText = StringVar()
callingText = StringVar()
callerRunningText = StringVar()


visitorData = ["000", "000", "000", "000"]
uniqueText = StringVar()
totalText = StringVar()
selectedMacro = StringVar()

master.title("Caller Client 1.0")
master.configure(bg="#111")

runningLabel = Label(master, bg="#111", fg="#FFF", textvariable=runningText,
                     justify=CENTER, font=infoFont)
runningLabel.grid(sticky=NW, row=1, column=0, columnspan=2, padx=10, pady=10)

callerRunningLabel = Label(master, bg="#111", fg="#FFF", textvariable=callerRunningText,
                           justify=CENTER, font=infoFont)
callerRunningLabel.grid(sticky=NW, row=2, column=0,
                        columnspan=2, padx=10, pady=10)

start_button = Button(master, text="Start Caller",
                      command=start_caller, font=infoFont)
start_button.grid(sticky=NW, row=3, column=0,
                  padx=10, pady=10, ipadx=10, ipady=5)

exit_all_button = Button(master, text="Exit All",
                         command=exit_all, font=infoFont)
exit_all_button.grid(sticky=NW, row=4, column=0,
                     padx=10, pady=10, ipadx=10, ipady=5)

exit_button = Button(master, text="Exit Caller Now",
                     command=exit_caller_now, font=infoFont)
exit_button.grid(sticky=NW, row=3, column=1,
                 padx=10, pady=10, ipadx=10, ipady=5)

#exit_chrome_button = Button(master, text="Exit Chrome",
#                            command=exit_chrome, font=infoFont)
#exit_chrome_button.grid(sticky=NW, row=3, column=1,
#                        padx=10, pady=10, ipadx=10, ipady=5)

exit_cleanup_button = Button(master, text="Exit Caller & Cleanup",
                             command=exit_cleanup, font=infoFont)
exit_cleanup_button.grid(sticky=NW, row=4, column=1,
                         padx=10, pady=10, ipadx=10, ipady=5)

callingLabel = Label(master, bg="#111", fg="#FFF", textvariable=callingText,
                     justify=CENTER, font=infoFont)
callingLabel.grid(sticky=NW, row=5, column=0, columnspan=1, padx=10, pady=10)

callOutcome = Label(master, bg="#111", fg="#FFF", textvariable=outcomeText,
                    justify=CENTER, font=infoFont)
callOutcome.grid(sticky=NW, row=5, column=1, columnspan=1, padx=10, pady=10)


def on_closing():
    master.destroy()


master.wait_visibility()
check_overwatch_status()
master.protocol('WM_DELETE_WINDOW', on_closing)
mainloop()

# sio.wait()
