import os
import sys

# Dynamically append current working directory to sys.path to guarantee package resolution
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import argparse
from eval_harness import EvaluationHarness, JUnitReporter


def main():
    parser = argparse.ArgumentParser(description="SIL System Evaluation Harness")
    parser.add_argument("--sut", required=True, help="Path to executable binary")
    parser.add_argument("--tests", required=True, help="Directory containing scenario JSON files")
    parser.add_argument("--output-xml", default="reports/junit.xml", help="Output JUnit XML path")
    args = parser.parse_args()

    harness = EvaluationHarness(sut_binary=args.sut, test_dir=args.tests)
    results = harness.run_suite()

    os.makedirs(os.path.dirname(os.path.abspath(args.output_xml)), exist_ok=True)
    JUnitReporter.export(results, args.output_xml)

    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    print(f"\n[+] Evaluation Suite Complete: {passed}/{total} Scenarios Passed.")

    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()