#!/usr/bin/python3

from pyaudio import PyAudio, paUInt8
from tkinter import Tk, Entry

# Constants
SAMPLE_RATE = 8448
CHANNELS = 1
BUFFER_SIZE = 256
CHECK_INTERVAL = 1024

class AudioGenerator:
    def __init__(self, sample_rate=SAMPLE_RATE, channels=CHANNELS):
        self.audio_interface = PyAudio()
        self.audio_stream = self.audio_interface.open(
            format=paUInt8,
            channels=channels,
            rate=sample_rate,
            output=True
        )
        self.time = 0
        self.formula = 't'

    def generate_audio_values(self):
        audio_values = []
        for _ in range(BUFFER_SIZE):
            audio_values.append(0xFF & eval(self.formula, {'t': self.time}))
            self.time += 1
        return audio_values

    def update_formula(self, user_input):
        try:
            assert(isinstance(eval(user_input, {'t': 0}), int))
            self.formula = user_input
            return 'green'
        except:
            return 'red'

    def close(self):
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio_interface.terminate()

class AudioApp:
    def __init__(self, root, audio_generator):
        self.root = root
        self.audio_generator = audio_generator
        self.formula_entry = Entry(root, width=48)
        self.formula_entry['font'] = ('Terminus', 24)
        self.formula_entry.insert(0, 't')
        self.formula_entry.focus()
        self.formula_entry.pack()
        self.is_running = True
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.is_running = False
        self.audio_generator.close()
        self.root.destroy()

    def run(self):
        while self.is_running:
            if self.audio_generator.time % CHECK_INTERVAL == 0:
                if self.audio_generator.time >> 21:
                    self.audio_generator.time = 0
                user_input = self.formula_entry.get()
                self.formula_entry['fg'] = self.audio_generator.update_formula(user_input)

            audio_values = self.audio_generator.generate_audio_values()
            self.audio_generator.audio_stream.write(bytes(audio_values))
            self.root.update()

if __name__ == "__main__":
    root = Tk()
    audio_generator = AudioGenerator()
    app = AudioApp(root, audio_generator)
    app.run()
