import threading
import time


class ReaderThread(threading.Thread):
    def __init__(self, dev, sample_interval_s, stop_token, out_lock):
        super().__init__(daemon=True)
        self.dev = dev
        self.sample_interval_s = sample_interval_s
        self.stop_token = stop_token
        self.out_lock = out_lock

    def run(self):
        self.dev.open()
        try:
            while not self.stop_token.stopped():
                start = time.monotonic()

                data = self.dev.read_chunk(16)
                ts = time.strftime("%H:%M:%S", time.localtime())

                with self.out_lock:
                    print(f"[scope] {ts}  {data.hex(' ')}")

                elapsed = time.monotonic() - start
                remaining = self.sample_interval_s - elapsed
                if remaining > 0:
                    time.sleep(remaining)

        finally:
            self.dev.close()
            with self.out_lock:
                print("[scope] reader stopped")
