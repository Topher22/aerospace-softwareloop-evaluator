import os
import json
import time
from typing import List
from .runner import SILRunner
from .evaluator import MetricEvaluator
from .models import TestCaseResult, EvalMetric

class EvaluationHarness:
    def __init__(self, sut_binary: str, test_dir: str):
        self.sut_binary = sut_binary
        self.test_dir = test_dir

    def run_suite(self) -> List[TestCaseResult]:
        suite_results: List[TestCaseResult] = []
        scenario_files = sorted([f for f in os.listdir(self.test_dir) if f.endswith(".json")])

        for scenario_file in scenario_files:
            file_path = os.path.join(self.test_dir, scenario_file)

            with open(file_path, "r", encoding="utf-8") as f:
                scenario_data = json.load(f)

            # Unterstützt Jira-Key und klassische Felder
            jira_key = scenario_data.get("test_key") or scenario_data.get("jira_key", "")
            test_id = scenario_data.get("scenario_name") or scenario_data.get("test_id", scenario_file)
            steps = scenario_data.get("steps", [])

            runner = SILRunner(self.sut_binary)
            
            start_time = time.perf_counter()
            telemetry_frames = runner.execute_interactive_scenario(steps)
            duration_ms = (time.perf_counter() - start_time) * 1000.0

            all_metrics: List[EvalMetric] = []
            scenario_passed = True

            if not telemetry_frames or len(telemetry_frames) != len(steps):
                scenario_passed = False

            # Schrittweise Telemetrie gegen die jeweiligen Sollwerte prüfen
            for i, frame in enumerate(telemetry_frames):
                step_bounds = steps[i].get("expected", {})
                frame_metrics = MetricEvaluator.evaluate_telemetry(frame, step_bounds)
                for metric in frame_metrics:
                    all_metrics.append(metric)
                    if not metric.passed:
                        scenario_passed = False

            suite_results.append(
                TestCaseResult(
                    test_id=test_id,
                    jira_key=jira_key,
                    passed=scenario_passed,
                    metrics=all_metrics,
                    duration_ms=round(duration_ms, 2)
                )
            )

        return suite_results