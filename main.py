import keyboard

from threading import Timer
from datetime import datetime
from collection import deque

# Wrapper for keyboard events
# Contains any necessary formatting logic
class KeyPress:
    def __init__(self, _type, code, ts=datetime.today(), raw=''):
        self.raw = raw
        self.type = _types
        self.ts = ts
        self.code = code

    def __repr__(self):
        return f'{self.type}\t{self.code}\t{self.ts}'
    
    def __str__(self):
        return f'{self.type}\t{self.code}\t{self.ts}'
    
class Sink:
    def write(self, kp): raise NotImplementedError

class ConsoleSink(Sink):
    def write(self, kp):
        msg = kp.to_string()
        print(msg)

class KeyLogger:
    def __init__(self, sink):
        self.sink = sink
        # A simple stack for capturing key strokes
        # this will help massage out chords and shortcuts
        self.stack = []

    # Create KeyPress objs from keyboard events
    # Then pipe them into a Sink
    def capture(self, event):
        kp = KeyPress(_type=event.event_type, code=event.name, raw=event.to_json())

        """ 
            - We got a new key event, could be up or down
            - If K  '/ m//  /'// / /' ' /i '  n    - push (`pop + new_code`)
                - if stack < 1
                    - push ( new_code )
            - if KEY_UP
                - if stack = 1 and pop = same code
                    Log the code
                - if stack > 1
                    - 
        """
        if kp._type == keyboard.KEY_DOWN:
            if len(self.stack) > 0:
                while 

        self.sink.write(kp)

    def start(self):
        keyboard.hook(callback=self.capture)
        keyboard.wait()

if __name__ == "__main__":
    cs = ConsoleSink()
    keylogger = KeyLogger(sink=cs)
    keylogger.start()

