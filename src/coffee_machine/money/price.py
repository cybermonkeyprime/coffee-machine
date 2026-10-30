from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class Price:
    amount: float
