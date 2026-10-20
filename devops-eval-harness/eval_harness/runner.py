import os
import json
import subprocess
from typing import List, Dict, Any

class SILRunner:
    def __init__(self, sut_binary: str):
        self.sut_binary = os.path.abspath(sut_binary)

    def execute_interactive_scenario(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not os.path.exists(self.sut_binary):
            raise FileNotFoundError(f"SUT binary not found at: {self.sut_binary}")

        process = subprocess.Popen(
            [self.sut_binary],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        telemetry_frames = []

        for step in steps:
            stimulus = step.get("input", {})
            process.stdin.write(json.dumps(stimulus) + "\n")
            process.stdin.flush()

            response_line = process.stdout.readline()
            if response_line:
                telemetry_frames.append(json.loads(response_line.strip()))
            else:
                break

        process.terminate()
        process.wait()

        return telemetry_frames