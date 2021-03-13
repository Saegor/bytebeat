#!/usr/bin/python3

from pyaudio import PyAudio, paUInt8
from tkinter import Tk, Entry


pa = PyAudio()
audio = pa.open(
    format = paUInt8,
    channels = 1,
    rate = 8448,
    output = True
)

tk = Tk()

entry = Entry(tk, width = 3 << 4)
entry['font'] = 'Terminus', 24
entry.insert(0, 't')
entry.focus()
entry.pack()

run = True
def close():
    global run
    run = False
tk.protocol("WM_DELETE_WINDOW", close)

time = 0
while run:

    if time % 0x400 == 0:
        if time >> 21 : time = 0
        try:
            e = entry.get()
            assert(isinstance(eval(e, {'t': 0}), int))
            formula = e
            entry['fg'] = 'green'
        except:
            entry['fg'] = 'red'

    values = []
    for _i in range(0x100):
        values.append(0xFF & eval(formula, {'t': time}))
        time += 1

    audio.write(bytes(values))
    tk.update()
