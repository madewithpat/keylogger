import keyboard
import re

from threading import Timer
from datetime import datetime
from functools import reduce

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
        return f'{self.type}\t{self.name}\t{self.code}\t{self.ts}\t{self.raw}'
    
    def __str__(self):
        return f'{self.type}\t{self.name}\t{self.code}\t{self.ts}\t{self.raw}'

    def __eq__(self, other):
        return (
            isinstance(other, KeyPress)
            and self.type == other.type
            and self.code == other.code
        )
    
    def join(self, other):
        self.name = f'{self.name}+{other.name}'
        self.code = f'{self.code}+{other.code}'

    def isMod(self):
        modPattern = '([Cc]trl|windows|[Ss]hift|[Aa]lt)'
        return re.search(modPattern, self.name)
    
class Sink:
    def write(self, kp): raise NotImplementedError

class ConsoleSink(Sink):
    def write(self, kp):
        print(kp)


class KeyLogger:
    def __init__(self, sink):
        self.sink = sink

        self.downKeys = []
        self.outputKeys = []
        self.mods = []
        self.outputMods = []

    # Create KeyPress objs from keyboard events
    # Then pipe them into a Sink
    def capture(self, event):
        kp = KeyPress(_type=event.event_type, name=event.name, code=event.scan_code, raw=event.to_json())

        if kp.type == keyboard.KEY_DOWN:
            if kp.isMod():
                self.mods.append(kp)
                self.outputMods.append(kp)
            elif kp not in self.downKeys:
                self.downKeys.append(kp)
                self.outputKeys.append(kp)

        elif kp.type == keyboard.KEY_UP:
            """
            Rolls
            - key 1 down, key 2 down, key 1 up, key 2 up
            - key 1 is not a mod
            - the down keypress controls the order, not the up
            chords
            - key 1..n down where 1..n represents some number of mods
            - key a..z down where a..b represents non-mods
            - order doesn't matter, except that mods precede taps for output writing

            on key up
            - if there are no keys in down or mods, write the output keys
            - if the up key is in down, remove it
            - if the up key is in mods, remove it
            """
            isLastKey = (len(self.mods) + len(self.downKeys)) == 1

            if kp.isMod():
                self.mods.remove(kp)
            else:
                self.downKeys.remove(kp)

            if isLastKey:
                self.writeOutputKeys()

    def start(self):
        keyboard.hook(callback=self.capture)
        keyboard.wait()

    def writeOutputKeys(self):
        # Join outputMods
        # Join outputKeys
        # flush both
        # write to sink
        newKp = self.outputKeys.pop()
        if len(self.outputKeys) > 0:
            finalKp = reduce(lambda acc, next: acc.join(next), self.outputKeys)
            self.sink.write(finalKp)
        else:
            self.sink.write(newKp);
