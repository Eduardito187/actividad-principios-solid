from __future__ import annotations
from dataclasses import dataclass
from dto.register_patient_dto import RegisterPatientDTO
from src.app.result import Result
from src.domain.contracts.repositories import PatientRepository
from src.domain.contracts.notification import NotificationChannel
from src.domain.contracts.audit import AuditLogger
from src.domain.entities.patient import Patient
from src.domain.entities.value_objects import PatientId

@dataclass
class RegisterPatient:
    patients: PatientRepository
    notifier: NotificationChannel
    logger: AuditLogger


    def __call__(self, dto: RegisterPatientDTO) -> tuple[Result, PatientId | None]:
        if self.patients.find_by_email(dto.email):
            return Result(False, "email already registered"), None
        pid = self.patients.next_id()
        patient = Patient(pid, dto.name, dto.email, dto.phone)
        self.patients.save(patient)
        self.notifier.send(dto.email, "Bienvenido a Salud Vital", "Registro completado.")
        self.logger.info("patient.registered", {"id": str(pid)})
        return Result(True, "registered"), pid