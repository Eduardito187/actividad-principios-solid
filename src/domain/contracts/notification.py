from __future__ import annotations
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, to, subject: str, message: str) -> None: ...