from dataclasses import dataclass
from typing import List

@dataclass
class ValidationResult:
    ok: bool
    reasons: List[str]

def ok() -> ValidationResult:
    return ValidationResult(True, [])

def fail(*reasons: str) -> ValidationResult:
    return ValidationResult(False, list(reasons))

def round_to_multiple(qty: int, multiple: int) -> int:
    if multiple <= 1:
        return int(qty)
    m = int(multiple)
    return int(((qty + m - 1) // m) * m)
