import argparse
from eval_harness import EvaluationHarness, JUnitReporter

def main():
    parser = argparse.ArgumentParser(description="SIL Evaluation Test Suite")
    parser.add_argument("--sut", required=True, help="Pfad zum SUT-Binary")
    parser.add_argument("--tests", required=True, help="Verzeichnis der Test-Szenarien")
    parser.add_argument("--output-xml", default="reports/junit.xml", help="Ausgabepfad für JUnit XML")
    args = parser.parse_args()

    harness = EvaluationHarness(sut_binary=args.sut, test_dir=args.tests)
    results = harness.run_suite()

    passed_count = sum(1 for r in results if r.passed)
    total_count = len(results)

    for r in results:
        print(f"[{r.status}] {r.jira_key} - {r.test_id} ({r.duration_ms} ms)")
        if not r.passed:
            for m in r.metrics:
                if not m.passed:
                    print(f"    -> Fehler: {m.name} = {m.value}{m.unit} (Soll: [{m.min_bound}, {m.max_bound}])")

    JUnitReporter.export(results, args.output_xml)
    print(f"\n[+] Evaluation Suite Complete: {passed_count}/{total_count} Scenarios Passed.")

if __name__ == "__main__":
    main()