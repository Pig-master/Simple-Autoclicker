import tkinter as tk
import sched, time
import pyautogui
import threading
import random
from pynput.keyboard import Key, Listener

root = tk.Tk()
root.title("Autoclicker")

run = 0
timeperclick = 1
timeperclickbase = 1
clickingtype = "Left Click"

varmin = 0
varmax = 0

my_scheduler = sched.scheduler(time.time, time.sleep)

def onoff(event=None):
    global run
    global clickingtype
    clickingtype = selected.get()
    print(clickingtype)
    if run == 0:
        run = 1
        startbtn.config(text="Stop (F6)")
        threading.Thread(target=start_scheduler).start()
    else:
        run = 0
        startbtn.config(text="Start (F6)")

def do_something(scheduler):
    if run == 1:
        global timeperclick
        global timeperclickbase
        global varmax
        global varmin
        timeperclick = timeperclickbase
        timeperclick += random.uniform(varmin, varmax)
        print(timeperclick)
        global clickingtype
        if clickingtype == "Right Click":
            scheduler.enter(timeperclick, 1, do_something, (scheduler,))
            print("Clicked RMB")
            pyautogui.rightClick()
        if clickingtype == "Left Click":
            scheduler.enter(timeperclick, 1, do_something, (scheduler,))
            print("Clicked LMB")
            pyautogui.click()
        if clickingtype == "Middle Click":
            scheduler.enter(timeperclick, 1, do_something, (scheduler,))
            print("Clicked MMB")
            pyautogui.middleClick()

def start_scheduler():
    global my_scheduler
    while run == 1:
        my_scheduler.enter(timeperclick, 1, do_something, (my_scheduler,))
        my_scheduler.run()
        if not run:
            break

def setval():
    global timeperclick
    global timeperclickbase
    text = timeval.get()
    if text:
        timeperclick = float(timeval.get())
        timeperclickbase = float(timeval.get())
        print(timeperclick)

def setrandval():
    global varmax
    global varmin
    text1 = valuemin.get()
    if text1:
        varmin = float(valuemin.get())
    text2 = valuemax.get()
    if text2:
        varmax = float(valuemax.get())

def on_closing():
    global run
    run = 0
    root.destroy()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.resizable(False, False)

frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")

frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)

lbl = tk.Label(frame, text="Autoclicker")
lbl.grid(row=0, column=0, columnspan=3, sticky="ew")

startbtn = tk.Button(frame, text="Start (F6)", command=onoff)
startbtn.grid(row=1, column=0, columnspan=3, sticky="ew")

lbl2 = tk.Label(frame, text="Time Per Click (Seconds)")
lbl2.grid(row=2, column=0)

timeval = tk.Entry(frame)
timeval.grid(row=2, column=1)

valuemin = tk.Entry(frame)
valuemin.grid(row=4, column=1)

valuemax = tk.Entry(frame)
valuemax.grid(row=4, column=2)

valueminlbl = tk.Label(frame, text="Rand Variation Min")
valueminlbl.grid(row=3, column=1)

valuemaxlbl = tk.Label(frame, text="Rand Variation Max")
valuemaxlbl.grid(row=3, column=2)

valbtn = tk.Button(frame, text="Set", command=setval)
valbtn.grid(row=2, column=2, sticky="w")

valrandbtn = tk.Button(frame, text="Set", command=setrandval)
valrandbtn.grid(row=5, column=1, columnspan=2, sticky="we")

selected = tk.StringVar()
lc = tk.Radiobutton(frame, text='Left Click', value='Left Click', variable=selected)
rc = tk.Radiobutton(frame, text='Right Click', value='Right Click', variable=selected)
mc = tk.Radiobutton(frame, text='Middle Click', value='Middle Click', variable=selected)
lc.grid(row=3, column=0)
rc.grid(row=4, column=0)
mc.grid(row=5, column=0)
selected.set("Left Click")

def pp(key):
    global keybind
    if key == Key.f6:
        onoff()

listener_thread = threading.Thread(target=lambda: Listener(on_press=pp).start())
listener_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.attributes("-topmost", True)
root.focus_force()

root.mainloop()
