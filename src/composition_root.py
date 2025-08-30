from __future__ import annotations
from datetime import datetime, timedelta
from uuid import uuid4
from src.domain.entities.value_objects import EmailAddress, PhoneNumber
from src.domain.policies.scheduling_policy import SimpleNoOverlapPolicy
from src.infrastructure.logging.std_logger import StdLogger
from src.infrastructure.notification.composite_notifier import CompositeNotifier
from src.infrastructure.notification.email_channel import EmailChannel
from src.infrastructure.notification.sms_channel import SmsChannel
from src.infrastructure.notification.whatsapp_channel import WhatsappChannel
from src.infrastructure.persistence.in_memory.doctor_repo import InMemoryDoctorRepository
from src.infrastructure.time.system_clock import SystemClock
from src.infrastructure.persistence.in_memory.appointment_repo import InMemoryAppointmentRepository
from src.infrastructure.persistence.in_memory.patient_repo import InMemoryPatientRepository
from src.domain.entities.patient import Patient
from src.domain.entities.doctor import Doctor
from src.domain.entities.specialties import Specialty
from src.app.dto.book_appointment_dto import BookAppointmentDTO
from src.app.use_cases.book_appointment import BookAppointment
from src.app.use_cases.approve_appointment import ApproveAppointment
from src.app.use_cases.doctor_agenda_query import DoctorAgendaQuery
from src.app.use_cases.cancel_appointment import CancelAppointment

def demo():
    patients = InMemoryPatientRepository()
    appointments = InMemoryAppointmentRepository()
    doctors = InMemoryDoctorRepository()
    notifier = CompositeNotifier([EmailChannel(), SmsChannel(), WhatsappChannel()])
    logger = StdLogger()
    clock = SystemClock()
    policy = SimpleNoOverlapPolicy()

    # Seed: doctor y paciente
    d = Doctor(
        id=doctors.next_id(),
        name="Dra. Pérez",
        specialty=Specialty.CARDIOLOGY,
        phone=PhoneNumber(value="79850175"),
        email=None
    )
    doctors.save(d)
    p = Patient(
        id=patients.next_id(),
        name="Juan Pérez",
        phone=PhoneNumber(value="63446080"),
        email=EmailAddress(value="eduardchavez302@gmail.com")
    )
    patients.save(p)

    # 1) Reservar
    start = datetime.now() + timedelta(hours=2)
    end   = start + timedelta(minutes=30)
    book = BookAppointment(appointments, patients, doctors, policy, notifier, logger, clock)
    res, appt_id = book(BookAppointmentDTO(
        patient_id=str(p.id),
        doctor_id=str(d.id),
        start=start,
        end=end
    ))

    # 2) Aprobar
    approve = ApproveAppointment(appointments, patients, notifier, logger)
    approve(str(appt_id))

    # 3) Agendar
    agenda = DoctorAgendaQuery(appointments, logger)
    agenda(str(d.id), day=start.strftime("%Y-%m-%d"))

    # 4) Cancelar
    cancel = CancelAppointment(appointments, patients, notifier, logger)
    cancel(str(appt_id))

if __name__ == "__main__":
    demo()