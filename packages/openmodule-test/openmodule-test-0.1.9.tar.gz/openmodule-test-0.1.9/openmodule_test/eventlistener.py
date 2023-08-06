import time
from unittest.mock import Mock


class MockEvent(Mock):
    _wait_sleep = 0.05

    def reset_call_count(self):
        self.call_count = 0

    def wait_for_call(self, timeout=3):
        assert self.call_count == 0, (
            "you must reset the call count first via .reset_call_count(), before sending any messages.\n"
            "This avoids a race condition"
        )
        for x in range(int(timeout // self._wait_sleep)):
            time.sleep(self._wait_sleep)
            if self.call_count > 0:
                return
        self.assert_called()
