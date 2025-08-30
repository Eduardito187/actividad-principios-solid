from __future__ import annotations
from abc import ABC, abstractmethod

class AuditLogger(ABC):
    @abstractmethod
    def info(self, event: str, context: dict | None = None) -> None: ...