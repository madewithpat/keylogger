# Simple Keylogger

I wrote a small keylogger to assist in designing keymaps for my keyboards.

## **DISCLAIMER**
This is a personal project, which I run on my own computer, to gather information about how I use my keyboard. I am not responsible for your usage of this code. Use at your own risk.

## Getting started

```sh
pip3 install -r requirements.txt
python keylogger.py
```

This will start a simple keylogger, which grabs keyboard events and outputs them to the console.

## Goals

1. All data stays local
2. Logged keystrokes are easy to read / analyze
3. Combinations and keyboard shortcuts are accurately recorded

## Implementation

The `keyboard` module in python seems like the simplest way to get this done. Essentially all I want is something that captures keyboard input, and pipes that to some sort of output (console, file, database, etc).

### Sink
Borrowing from some general logging concepts, I wrote a generic `Sink` "interface" (it's Python, but yeah). This just contains a `write` function, which accepts `KeyPress` objects. Piping keystrokes to a different destination is just a matter of implenting `Sink` and passing it to the `Keylogger` at instantiation.

### KeyPress
The `keyboard` module has a class for keyboard events, but I wanted some degree of control over how keystrokes are interpreted. E.g., I don't really care to see `Shift+[` when `{` is more accurate. This same mindset applies to shortcuts as well.

### Keylogger
The central piece of this project, though arguably one of the simpler parts. Accepts a `Sink` in the ctor, which will receive `KeyPress` objects created from keyboard events. `Keylogger.start()` sets up a listener with the `keyboard` module, which creates the `KeyPress` and sends it to the `Sink`.