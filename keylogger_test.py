import pytest
import keylogger
from keyboard import KeyboardEvent

class SpySink(keylogger.Sink):
    def __init__(self):
        self.codes = []

    def write(self, kp):
        self.codes.append(kp)

@pytest.fixture
def spy_sink():
    return SpySink()

@pytest.fixture
def sut(spy_sink):
    return keylogger.KeyLogger(spy_sink)

class TestKeyLogger:

    def test_logging_single_taps(self, sut, spy_sink):
        evt = KeyboardEvent(event_type='down', scan_code=31, name='test')
        sut.capture(evt)
        evt = KeyboardEvent(event_type='up', scan_code=31, name='test')
        sut.capture(evt)

        assert len(spy_sink.codes) == 1