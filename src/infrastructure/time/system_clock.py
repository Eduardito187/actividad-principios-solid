from __future__ import annotations
from datetime import datetime
from src.domain.contracts.clock import Clock


class SystemClock(Clock):
    def now(self) -> datetime:
        return datetime.now()