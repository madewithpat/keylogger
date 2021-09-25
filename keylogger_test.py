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

# Some basic key strokes for testing
ctrl_dn = KeyboardEvent(event_type='down', scan_code=29, name='ctrl')
ctrl_up = KeyboardEvent(event_type='up', scan_code=29, name='ctrl')
k_dn = KeyboardEvent(event_type='down', scan_code=37, name='k')
k_up = KeyboardEvent(event_type='up', scan_code=37, name='k')
shift_dn = KeyboardEvent(event_type='down', scan_code=42, name='shift')
shift_up = KeyboardEvent(event_type='up', scan_code=42, name='shift')

class TestKeyLogger:

    def test_logging_single_taps(self, sut, spy_sink):
        sut.capture(k_dn)
        sut.capture(k_up)

        captured = spy_sink.codes[0]
        assert len(spy_sink.codes) == 1
        assert captured.code == k_up.scan_code

    def test_logging_modifiers(self, sut, spy_sink):
        sut.capture(ctrl_dn)
        sut.capture(k_dn)
        sut.capture(k_up)
        sut.capture(ctrl_up)

        assert len(spy_sink.codes) == 1
        captured = spy_sink.codes[0]
        assert captured.name == 'ctrl+k'