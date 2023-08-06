import time
from _weakrefset import WeakSet
from unittest.mock import Mock

_all_mocks = WeakSet()


class MockEvent(Mock):
    _wait_sleep = 0.05

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _all_mocks.add(self)

    @staticmethod
    def reset_all_call_counts():
        for x in _all_mocks:
            x.reset_call_count()

    def reset_call_count(self):
        self.call_count = 0

    def wait_for_call(self, timeout=3):
        for x in range(int(timeout // self._wait_sleep)):
            time.sleep(self._wait_sleep)
            if self.call_count > 0:
                return
        self.assert_called()
