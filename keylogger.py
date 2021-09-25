import keyboard

from threading import Timer
from datetime import datetime

# Wrapper for keyboard events
# Contains any necessary formatting logic
class KeyPress:
    def __init__(self, _type, name, code, ts=datetime.today(), raw=''):
        self.raw = raw
        self.type = _type
        self.ts = ts
        self.name = name
        self.code = code

    def __repr__(self):
        return f'{self.type}\t{self.name}\t{self.code}\t{self.ts}'
    
    def __str__(self):
        return f'{self.type}\t{self.name}\t{self.code}\t{self.ts}'

    def __eq__(self, other):
        return (
            isinstance(other, KeyPress)
            and self.type == other.type
            and self.code == other.code
        )
    
class Sink:
    def write(self, kp): raise NotImplementedError

class ConsoleSink(Sink):
    def write(self, kp):
        print(kp)


class KeyLogger:
    def __init__(self, sink):
        self.sink = sink
        # A simple stack for capturing key strokes
        # this will help massage out chords and shortcuts
        self.held = []
        self.tapped = []
        self.output = None

    # Create KeyPress objs from keyboard events
    # Then pipe them into a Sink
    def capture(self, event):
        kp = KeyPress(_type=event.event_type, name=event.name, code=event.scan_code, raw=event.to_json())

        if kp.type == keyboard.KEY_DOWN:
            self.tapped.append(kp)
        elif kp.type == keyboard.KEY_UP:
            prev = self.tapped.pop()
            if (prev.code == kp.code):
                self.sink.write(kp)

    def start(self):
        keyboard.hook(callback=self.capture)
        keyboard.wait()