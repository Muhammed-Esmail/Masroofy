from dataclasses import dataclass

@dataclass
class Settings:
    currency: str
    cycle_duration: int
    budget_threshold: int
    language: str
    theme: str