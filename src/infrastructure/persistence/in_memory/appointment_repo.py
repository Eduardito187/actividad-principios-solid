from __future__ import annotations
from typing import Dict
from uuid import uuid4
from src.domain.contracts.repositories import AppointmentRepository
from src.domain.entities.appointment import Appointment
from src.domain.entities.value_objects import AppointmentId, DoctorId, TimeSlot


class InMemoryAppointmentRepository(AppointmentRepository):
    def __init__(self) -> None:
        self._db: Dict[AppointmentId, Appointment] = {}

    def next_id(self) -> AppointmentId:
        return uuid4()

    def save(self, appt: Appointment) -> None:
        self._db[appt.id] = appt

    def find_by_id(self, aid: AppointmentId) -> Appointment | None:
        return self._db.get(aid)

    def for_doctor_and_day(self, did: DoctorId, day: str) -> list[Appointment]:
        return [a for a in self._db.values() if a.doctor_id == did and a.slot.start.strftime('%Y-%m-%d') == day]

    def overlapping_for_doctor(self, did: DoctorId, slot: TimeSlot) -> list[Appointment]:
        return [a for a in self._db.values() if a.doctor_id == did and a.slot.overlaps(slot)]