from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence
from src.domain.entities.value_objects import TimeSlot
from src.domain.entities.appointment import Appointment


class SchedulingPolicy(ABC):
    @abstractmethod
    def validate(self, slot: TimeSlot, existing: Sequence[Appointment]) -> list[str]:
        """Devuelve lista de problemas. Vacío => válido."""
        ...

class SimpleNoOverlapPolicy(SchedulingPolicy):
    def validate(self, slot: TimeSlot, existing: Sequence[Appointment]) -> list[str]:
        problems: list[str] = []
        if any(slot.overlaps(a.slot) for a in existing):
            problems.append("slot overlaps existing appointment")
        return problems