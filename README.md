# requirementsreadwrite

# Oscilloscope & Function Generator – Python (reqfRead / reqfWrite)

Implements `reqfRead` and `reqfWrite` in Python with a file-backed mock device.
CLI supports **acquire** and **generate**; prints bytes, duration, throughput, and latency percentiles (read).

## Setup
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt



## Install
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -e .

## One-shot commands
python -m oscifgen acquire --in input.bin --out capture.bin --fs 1000 --n 8192
python -m oscifgen generate --out tx.out --fo 2000 --n 4096 --wave square --amp 1.0

## Command file (UI macro) — satisfies Homework 6
python -m oscifgen run --script scripts/demo.json

# Expected prints
# START (acquire) launched in background.
# WAIT done.
# STOP complete (joined background job).
# WRITE bytes=... time_s=... throughput_Bps=...
