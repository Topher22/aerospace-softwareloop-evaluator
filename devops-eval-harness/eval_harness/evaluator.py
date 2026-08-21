# eval_harness/evaluator.py
from typing import Dict, Any, List
from .models import EvalMetric

class MetricEvaluator:
    @staticmethod
    def evaluate_telemetry(telemetry: Dict[str, Any], bounds: Dict[str, Any]) -> List[EvalMetric]:
        results = []
        for metric_name, bound_config in bounds.items():
            if metric_name not in telemetry:
                continue

            raw_data = telemetry[metric_name]
            
            # Unpack nested dict {"value": 25.7, "unit": "V"} or direct float/int
            if isinstance(raw_data, dict):
                val = float(raw_data.get("value", 0.0))
                unit = raw_data.get("unit", "")
            else:
                val = float(raw_data)
                unit = bound_config.get("unit", "")

            min_val = bound_config.get("min")
            max_val = bound_config.get("max")

            passed = True
            if min_val is not None and val < min_val:
                passed = False
            if max_val is not None and val > max_val:
                passed = False

            results.append(
                EvalMetric(
                    name=metric_name,
                    value=val,
                    unit=unit,
                    min_bound=min_val,
                    max_bound=max_val,
                    passed=passed
                )
            )
        return results