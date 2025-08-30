from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID
from src.app.result import Result
from src.domain.contracts.repositories import AppointmentRepository, PatientRepository
from src.domain.contracts.audit import AuditLogger
from src.domain.contracts.notification import NotificationChannel

@dataclass
class CancelAppointment:
    appointments: AppointmentRepository
    patients: PatientRepository
    notifier: NotificationChannel
    logger: AuditLogger

    def __call__(self, appointment_id: str) -> Result:
        appt = self.appointments.find_by_id(UUID(appointment_id))
        if not appt:
            return Result(False, "appointment not found")
        appt.cancel()
        self.appointments.save(appt)
        patient = self.patients.find_by_id(appt.patient_id)
        self.notifier.send(patient, "Cita cancelada", "Su cita fue cancelada.")
        self.logger.info("appointment.cancelled", {"id": appointment_id})
        return Result(True, "cancelled")