from typing import Dict, Any, List, Optional
from .models import EvalMetric

class MetricEvaluator:
    @staticmethod
    def _resolve_nested_value(data: Dict[str, Any], path: str) -> Optional[Any]:
        parts = path.split(".")
        curr = data
        for p in parts:
            if isinstance(curr, dict) and p in curr:
                curr = curr[p]
            else:
                return None
        return curr

    @classmethod
    def evaluate_telemetry(cls, telemetry: Dict[str, Any], bounds: Dict[str, Any]) -> List[EvalMetric]:
        results: List[EvalMetric] = []
        
        for metric_name, bound_config in bounds.items():
            # Punkt-Notation auflösen (z. B. "core_temperature.value")
            val_raw = cls._resolve_nested_value(telemetry, metric_name)
            
            # Falls nicht über Punkt erreichbar, direkten Schlüssel prüfen
            if val_raw is None and metric_name in telemetry:
                val_raw = telemetry[metric_name]

            if val_raw is None:
                results.append(
                    EvalMetric(
                        name=metric_name,
                        value=0.0,
                        unit="",
                        min_bound=bound_config.get("min"),
                        max_bound=bound_config.get("max"),
                        passed=False
                    )
                )
                continue

            # Wert und Einheit extrahieren
            if isinstance(val_raw, dict):
                val = float(val_raw.get("value", 0.0))
                unit = val_raw.get("unit", bound_config.get("unit", ""))
            else:
                val = float(val_raw)
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