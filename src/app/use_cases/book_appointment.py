from __future__ import annotations
from dataclasses import dataclass
from src.app.dto.book_appointment_dto import BookAppointmentDTO
from src.app.result import Result
from src.domain.contracts.repositories import AppointmentRepository, PatientRepository, DoctorRepository
from src.domain.contracts.notification import NotificationChannel
from src.domain.contracts.audit import AuditLogger
from src.domain.contracts.clock import Clock
from src.domain.policies.scheduling_policy import SchedulingPolicy
from src.domain.entities.value_objects import TimeSlot
from src.domain.entities.appointment import Appointment
from src.domain.entities.value_objects import AppointmentId, PatientId, DoctorId
from uuid import UUID

@dataclass
class BookAppointment:
    appointments: AppointmentRepository
    patients: PatientRepository
    doctors: DoctorRepository
    policy: SchedulingPolicy
    notifier: NotificationChannel
    logger: AuditLogger
    clock: Clock

    def __call__(self, dto: BookAppointmentDTO) -> tuple[Result, AppointmentId | None]:
        patient = self.patients.find_by_id(UUID(dto.patient_id))
        doctor = self.doctors.find_by_id(UUID(dto.doctor_id))
        if not patient or not doctor:
            return Result(False, "patient or doctor not found"), None

        slot = TimeSlot(dto.start, dto.end)
        existing = self.appointments.overlapping_for_doctor(doctor.id, slot)
        problems = self.policy.validate(slot, existing)
        if problems:
            return Result(False, "; ".join(problems)), None

        appt_id = self.appointments.next_id()
        appt = Appointment(appt_id, patient.id, doctor.id, slot)
        self.appointments.save(appt)
        self.notifier.send(patient, "Reserva registrada", "Su solicitud fue recibida.")
        self.logger.info("appointment.booked", {"id": str(appt_id)})
        return Result(True, "booked"), appt_id