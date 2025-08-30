from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID
from typing import List
from src.domain.contracts.audit import AuditLogger
from src.app.result import Result
from src.domain.contracts.repositories import AppointmentRepository
from src.domain.entities.appointment import Appointment

@dataclass
class DoctorAgendaQuery:
    appointments: AppointmentRepository
    logger: AuditLogger

    def __call__(self, doctor_id: str, day: str) -> tuple[Result, List[Appointment]]:
        appts = self.appointments.for_doctor_and_day(UUID(doctor_id), day)
        for appt in appts:
            self.logger.info("doctor.agenda.query", appt)
        return Result(True, f"{len(appts)} appointments"), appts