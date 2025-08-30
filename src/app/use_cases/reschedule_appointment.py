from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from src.app.result import Result
from src.domain.contracts.repositories import AppointmentRepository, PatientRepository
from src.domain.contracts.audit import AuditLogger
from src.domain.contracts.notification import NotificationChannel
from src.domain.policies.scheduling_policy import SchedulingPolicy
from src.domain.entities.value_objects import TimeSlot

@dataclass
class RescheduleAppointment:
    appointments: AppointmentRepository
    patients: PatientRepository
    policy: SchedulingPolicy
    notifier: NotificationChannel
    logger: AuditLogger

    def __call__(self, appointment_id: str, start: datetime, end: datetime) -> Result:
        appt = self.appointments.find_by_id(UUID(appointment_id))
        if not appt:
            return Result(False, "appointment not found")
        new_slot = TimeSlot(start, end)
        existing = [a for a in self.appointments.overlapping_for_doctor(appt.doctor_id, new_slot) if a.id != appt.id]
        problems = self.policy.validate(new_slot, existing)
        if problems:
            return Result(False, "; ".join(problems))
        appt.reschedule(new_slot)
        self.appointments.save(appt)
        patient = self.patients.find_by_id(appt.patient_id)
        to = getattr(patient, 'email', str(appt.patient_id))
        self.notifier.send(to, "Cita reprogramada", "Su cita fue reprogramada.")
        self.logger.info("appointment.rescheduled", {"id": appointment_id})
        return Result(True, "rescheduled")