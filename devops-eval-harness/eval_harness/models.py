from dataclasses import dataclass
from typing import List, Optional

#defines core data schema for evaluation metrics and test case results. Each EvalMetric captures a specific measurement, its value, unit, thresholds, and pass/fail status. TestCaseResult aggregates multiple EvalMetrics along with test metadata like ID, Jira key, duration, status, and any error messages.
@dataclass
class EvalMetric:
    name: str
    value: float
    unit: str
    threshold_max: Optional[float] = None
    threshold_min: Optional[float] = None
    passed: bool = True

@dataclass
class TestCaseResult:
    test_id: str
    jira_key: str
    duration_ms: float
    status: str  # PASS, FAIL, ERROR
    metrics: List[EvalMetric]
    error_message: Optional[str] = None