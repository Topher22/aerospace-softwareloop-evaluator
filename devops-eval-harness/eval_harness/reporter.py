import xml.etree.ElementTree as ET
import os
from typing import List
from .models import TestCaseResult

class JUnitReporter:
    @staticmethod
    def export(results: List[TestCaseResult], output_path: str) -> None:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        testsuite = ET.Element("testsuite", name="SIL_Telemetry_Verification")
        
        for res in results:
            testcase = ET.Element(
                "testcase",
                classname="TelemetryBoundsCheck",
                name=res.test_id,
                time=str(round(res.duration_ms / 1000.0, 3))
            )
            
            # Embed Jira Requirement Key for Xray Traceability
            if res.jira_key:
                ET.SubElement(testcase, "property", name="test_key", value=res.jira_key)

            # Check boolean passed flag directly
            if not res.passed:
                failed_metrics = [m for m in res.metrics if not m.passed]
                failure_details = "\n".join([
                    f"Metric '{m.name}' out of bounds: value={m.value}{m.unit} (min={m.min_bound}, max={m.max_bound})"
                    for m in failed_metrics
                ])
                
                failure_elem = ET.SubElement(
                    testcase,
                    "failure",
                    message="Telemetry safety boundary violation detected"
                )
                failure_elem.text = failure_details or "Scenario execution failed without returned telemetry."

            testsuite.append(testcase)

        tree = ET.ElementTree(testsuite)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)