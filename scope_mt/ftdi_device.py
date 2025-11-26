import time


class MockFtdiDevice:
    def __init__(self):
        self._open = False

    def open(self):
        self._open = True

    def read_chunk(self, nbytes=16):
        if not self._open:
            raise RuntimeError("Device not open")

        now_ms = int(time.time() * 1000) & 0xFFFF
        return now_ms.to_bytes(2, "little") * (nbytes // 2)

    def close(self):
        self._open = False
