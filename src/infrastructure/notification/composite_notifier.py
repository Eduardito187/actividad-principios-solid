from __future__ import annotations
from typing import Sequence
from src.domain.contracts.notification import NotificationChannel

class CompositeNotifier(NotificationChannel):
    def __init__(self, channels: Sequence[NotificationChannel]) -> None:
        self._channels = list(channels)

    def send(self, to, subject: str, message: str) -> None:
        for c in self._channels:
            c.send(to, subject, message)