# oscifgen/ftdi_device.py
from __future__ import annotations
from dataclasses import dataclass

# Try to import pyftdi; allow running without hardware
try:
    from pyftdi.serialext import serial_for_url
except Exception:
    serial_for_url = None

@dataclass
class IOResult:
    bytes: int
    err: str | None = None

class FtdiDevice:
    def __init__(self) -> None:
        self._ser = None

    def open(self, url: str) -> bool:
        """Open FTDI URL like 'ftdi://::/1'."""
        if serial_for_url is None:
            print("[FTDI] pyftdi not installed or unavailable.")
            return False
        try:
            self._ser = serial_for_url(url, timeout=1)
            return True
        except Exception as e:
            print(f"[FTDI] open failed: {e}")
            self._ser = None
            return False

    def read(self, n: int) -> IOResult:
        if not self._ser:
            # Behave like EOF / no device to keep higher layers running
            return IOResult(bytes=0, err="no_device")
        try:
            data = self._ser.read(n)
            return IOResult(bytes=len(data), err=None)
        except Exception as e:
            return IOResult(bytes=-1, err=str(e))

    def write(self, buf: bytes) -> IOResult:
        if not self._ser:
            # Pretend we "wrote" to allow demos without hardware
            return IOResult(bytes=len(buf), err="no_device")
        try:
            n = self._ser.write(buf)
            return IOResult(bytes=int(n), err=None)
        except Exception as e:
            return IOResult(bytes=-1, err=str(e))

    def close(self) -> None:
        try:
            if self._ser:
                self._ser.close()
        finally:
            self._ser = None
