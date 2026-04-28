from datetime import date
from dataclasses import dataclass

@dataclass
class Cycle:
    id: int | None
    startDate: date
    endDate: date
    amount: int