from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class EvalMetric:
    name: str
    value: float
    unit: str = ""
    min_bound: Optional[float] = None
    max_bound: Optional[float] = None
    passed: bool = True

@dataclass
class TestCaseResult:
    test_id: str
    jira_key: str
    passed: bool
    metrics: List[EvalMetric] = field(default_factory=list)
    duration_ms: float = 0.0

    @property
    def status(self) -> str:
        return "PASS" if self.passed else "FAIL"