import json
from dataclasses import asdict
from typing import List
from xml.etree import ElementTree as ET
from .models import TestCaseResult


class JUnitReporter:
    """Generates JUnit XML formatted with Jira keys for Xray REST ingestion."""

    @staticmethod
    def export(results: List[TestCaseResult], output_path: str):
        testsuites = ET.Element("testsuites")
        suite = ET.SubElement(testsuites, "testsuite", name="SIL_Telemetry_Evaluation")

        for res in results:
            classname = f"{res.jira_key}::{res.test_id}" if res.jira_key else res.test_id
            case = ET.SubElement(
                suite,
                "testcase",
                name=res.test_id,
                classname=classname,
                time=str(round(res.duration_ms / 1000.0, 3))
            )

            if res.status != "PASS":
                failure = ET.SubElement(case, "failure", message=res.error_message or "Threshold Violation")
                failure.text = json.dumps([asdict(m) for m in res.metrics if not m.passed], indent=2)

        tree = ET.ElementTree(testsuites)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)