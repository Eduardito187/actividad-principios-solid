from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from src.app.dto.doctor_note import DoctorNote
from .value_objects import AppointmentId, PatientId, DoctorId, TimeSlot

class AppointmentStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

@dataclass
class Appointment:
    id: AppointmentId
    patient_id: PatientId
    doctor_id: DoctorId
    slot: TimeSlot
    status: AppointmentStatus = AppointmentStatus.PENDING
    note: DoctorNote | None = None

    def approve(self) -> None: self.status = AppointmentStatus.APPROVED
    def reject(self) -> None: self.status = AppointmentStatus.REJECTED
    def cancel(self) -> None: self.status = AppointmentStatus.CANCELLED
    def reschedule(self, new_slot: TimeSlot) -> None: self.slot = new_slot