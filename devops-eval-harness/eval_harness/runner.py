import os
import json
import time
import subprocess
from typing import Dict, Any


class SILRunner:
    """Executes compiled C++ SUT binaries in isolated subprocesses."""

    def __init__(self, binary_path: str, timeout_sec: int = 30):
        self.binary_path = binary_path
        self.timeout_sec = timeout_sec

    def execute_scenario(self, scenario_config_path: str) -> Dict[str, Any]:
        if not os.path.exists(self.binary_path):
            raise FileNotFoundError(f"SUT binary not found: {self.binary_path}")

        cmd = [self.binary_path, "--config", scenario_config_path]
        start_time = time.perf_counter()

        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_sec
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            if process.returncode != 0:
                return {
                    "status": "ERROR",
                    "duration_ms": elapsed_ms,
                    "error": f"Process exited with code {process.returncode}: {process.stderr.strip()}",
                    "telemetry": {}
                }

            telemetry_data = json.loads(process.stdout)
            return {
                "status": "COMPLETED",
                "duration_ms": elapsed_ms,
                "error": None,
                "telemetry": telemetry_data
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "ERROR",
                "duration_ms": self.timeout_sec * 1000.0,
                "error": f"Execution timed out after {self.timeout_sec}s",
                "telemetry": {}
            }
        except json.JSONDecodeError as err:
            return {
                "status": "ERROR",
                "duration_ms": (time.perf_counter() - start_time) * 1000.0,
                "error": f"Invalid telemetry JSON emitted by SUT: {err}",
                "telemetry": {}
            }