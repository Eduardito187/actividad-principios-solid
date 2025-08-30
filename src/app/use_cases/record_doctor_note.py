from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID
from src.app.result import Result
from src.domain.contracts.repositories import AppointmentRepository
from src.domain.contracts.audit import AuditLogger
from src.app.dto.doctor_note import DoctorNote

@dataclass
class RecordDoctorNote:
    appointments: AppointmentRepository
    logger: AuditLogger

    def __call__(self, appointment_id: str, title: str, summary: str) -> Result:
        appt = self.appointments.find_by_id(UUID(appointment_id))
        if not appt:
            return Result(False, "appointment not found")
        appt.note = DoctorNote(title, summary)
        self.appointments.save(appt)
        self.logger.info("appointment.note_added", {"id": appointment_id})
        return Result(True, "note recorded")