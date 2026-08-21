import os
import json
from typing import List
from .models import TestCaseResult
from .runner import SILRunner
from .evaluator import MetricEvaluator


class EvaluationHarness:
    """Discovers scenarios, runs SIL execution, and calculates test suite outcomes."""

    def __init__(self, sut_binary: str, test_dir: str):
        self.runner = SILRunner(sut_binary)
        self.test_dir = test_dir

    def run_suite(self) -> List[TestCaseResult]:
        suite_results = []
        scenario_files = [f for f in os.listdir(self.test_dir) if f.endswith(".json")]

        for scenario_file in scenario_files:
            file_path = os.path.join(self.test_dir, scenario_file)
            with open(file_path, "r") as f:
                scenario_data = json.load(f)

            test_id = scenario_data.get("test_id", scenario_file)
            jira_key = scenario_data.get("jira_key", "")
            bounds = scenario_data.get("bounds", {})
            stimuli = scenario_data.get("stimuli", [])

            exec_res = self.runner.execute_scenario(file_path)

            if exec_res["status"] == "ERROR":
                suite_results.append(
                    TestCaseResult(
                        test_id=test_id,
                        jira_key=jira_key,
                        duration_ms=exec_res["duration_ms"],
                        status="ERROR",
                        metrics=[],
                        error_message=exec_res["error"]
                    )
                )
                continue

            metrics = MetricEvaluator.evaluate_telemetry(exec_res["telemetry"], bounds)
            all_passed = all(m.passed for m in metrics)
            status = "PASS" if all_passed else "FAIL"

            error_msg = None
            if not all_passed:
                failed_metrics = [m.name for m in metrics if not m.passed]
                error_msg = f"Metrics exceeded safety bounds: {', '.join(failed_metrics)}"

            suite_results.append(
                TestCaseResult(
                    test_id=test_id,
                    jira_key=jira_key,
                    duration_ms=exec_res["duration_ms"],
                    status=status,
                    metrics=metrics,
                    error_message=error_msg
                )
            )

        return suite_results