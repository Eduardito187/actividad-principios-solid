from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence
from src.domain.entities.value_objects import TimeSlot
from src.domain.entities.appointment import Appointment


class SchedulingPolicy(ABC):
    @abstractmethod
    def validate(self, slot: TimeSlot, existing: Sequence[Appointment]) -> list[str]:
        ...

class SimpleNoOverlapPolicy(SchedulingPolicy):
    def validate(self, slot: TimeSlot, existing: Sequence[Appointment]) -> list[str]:
        problems: list[str] = []
        for appt in existing:
            if slot.overlaps(appt.slot):
                problems.append("The schedule conflicts with another appointment.")

        start_hour = slot.start.hour
        end_hour = slot.end.hour
        if start_hour < 8 or end_hour > 18:
            problems.append("The appointment is outside of business hours (08:00-18:00)")

        duration_minutes = (slot.end - slot.start).total_seconds() / 60
        if duration_minutes < 15:
            problems.append("The appointment must last at least 15 minutes")

        return problems