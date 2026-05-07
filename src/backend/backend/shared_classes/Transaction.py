from datetime import date
from dataclasses import dataclass

@dataclass
class Transaction:
    id: int | None
    amount: int
    cycle_id: int
    category_name: str
    log_date: date
    description: str
    note: str | None