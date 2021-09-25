# Simple Keylogger

I wrote a small keylogger to assist in designing keymaps for my keyboards.

## Goals

1. All data stays local
2. Logged keystrokes are easy to read / analyze
3. Combinations and keyboard shortcuts are accurately recorded

## Implementation

The `keyboard` module in python seems like the simplest way to get this done. Essentially all I want is something that captures keyboard input, and pipes that to some sort of output (console, file, database, etc).

### Sink
Borrowing from some general logging concepts, I wrote a generic `Sink` "interface" (it's Python, but yeah). This just contains a `write` function, which accepts `KeyPress` objects

### KeyPress
The `keyboard` module has a class for keyboard events, but I wanted some degree of control over how keystrokes are interpreted. E.g., I don't really care to see `Shift+[` when `{` is more accurate. This same mindset applies to shortcuts as well.

### Keylogger
The central piece of this project, though arguably one of the simpler parts. Accepts a `Sink` in the ctor, which will receive `KeyPress` objects created from keyboard events. `Keylogger.start()` sets up a listener with the `keyboard` module, which creates the `KeyPress` and sends it to the `Sink`.