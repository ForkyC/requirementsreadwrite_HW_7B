import json
import time
import threading
from .reader import Reader
from .writer import Writer
from .loopctl import LoopController

class ScriptRunner:
    """
    Executes a JSON command script with actions:
    start, wait, stop, read, write.
    Supports both threaded and one-shot operations.
    """

    def __init__(self, script_path):
        self.script_path = script_path
        self.active_thread = None
        self.loopctl = LoopController()

    def run(self):
        print(f"[ScriptRunner] Loading script: {self.script_path}")
        with open(self.script_path, "r") as f:
            script = json.load(f)

        sequence = script.get("sequence", [])
        for step in sequence:
            command = list(step.keys())[0]
            params = step[command]
            print(f"\n[ScriptRunner] Executing: {command.upper()}")

            if command == "start":
                self._start_thread(params)
            elif command == "wait":
                self._wait(params)
            elif command == "stop":
                self._stop()
            elif command == "read":
                self._read(params)
            elif command == "write":
                self._write(params)
            else:
                print(f"[WARN] Unknown command: {command}")

        print("\n[ScriptRunner] Script complete.")

    # ------------------ Command Handlers ------------------ #

    def _start_thread(self, params):
        """Launch acquisition or generation in a background thread"""
        mode = params.get("mode", "acquire")

        def worker():
            if mode == "acquire":
                Reader(**params).run()
            elif mode == "generate":
                Writer(**params).run()
            else:
                print(f"[WARN] Invalid start mode: {mode}")

        self.active_thread = threading.Thread(target=worker, daemon=True)
        self.active_thread.start()
        print(f"[ScriptRunner] START ({mode}) launched in background.")

    def _wait(self, params):
        """Pause execution for time or loop count"""
        seconds = params.get("seconds")
        loops = params.get("loops")
        if seconds:
            print(f"[ScriptRunner] WAIT for {seconds}s...")
            time.sleep(seconds)
        elif loops:
            print(f"[ScriptRunner] WAIT for {loops} loops (simulated)...")
            time.sleep(loops * 0.1)
        else:
            print("[ScriptRunner] WAIT missing time or loop count.")

    def _stop(self):
        """Stop active thread safely"""
        if self.active_thread:
            print("[ScriptRunner] STOP signal sent. Waiting for thread...")
            self.loopctl.stop()
            self.active_thread.join(timeout=3)
            self.active_thread = None
            print("[ScriptRunner] STOP complete.")
        else:
            print("[ScriptRunner] No active thread to stop.")

    def _read(self, params):
        """One-shot FTDI read"""
        print("[ScriptRunner] READ operation:")
        Reader(**params).run()

    def _write(self, params):
        """One-shot FTDI write"""
        print("[ScriptRunner] WRITE operation:")
        Writer(**params).run()
