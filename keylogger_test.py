import keylogger
from keyboard import KeyboardEvent

class SpySink(keylogger.Sink):
    def __init__(self):
        self.codes = []

    def write(self, kp):
        self.codes.append(kp)

spy = SpySink()
sut = keylogger.KeyLogger(spy)

class TestKeyLogger:

    def test_keycode_logging(self):
        evt = KeyboardEvent(event_type='down', scan_code=31, name='test')
        sut.capture(evt)
        evt = KeyboardEvent(event_type='up', scan_code=31, name='test')
        sut.capture(evt)

        assert len(spy.codes) == 1