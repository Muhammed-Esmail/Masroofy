from datetime import date
from dataclasses import dataclass

@dataclass
class Transaction:
    id: int | None
    amount: int
    category_id: int
    log_date: date
    description: str
    note: str | None