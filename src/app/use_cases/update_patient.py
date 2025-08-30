from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID
from src.domain.entities.value_objects import EmailAddress, PhoneNumber
from dto.update_patient_dto import UpdatePatientDTO
from src.app.result import Result
from src.domain.contracts.repositories import PatientRepository
from src.domain.contracts.audit import AuditLogger

@dataclass
class UpdatePatient:
    patients: PatientRepository
    logger: AuditLogger

    def __call__(self, dto: UpdatePatientDTO) -> Result:
        patient = self.patients.find_by_id(UUID(dto.patient_id))
        if not patient:
            return Result(False, "patient not found")
        if dto.name is not None:
            patient.name = dto.name
        if dto.email is not None:
            patient.email = EmailAddress(value=dto.email)
        if dto.phone is not None:
            patient.phone = PhoneNumber(value=dto.phone)
        self.patients.save(patient)
        self.logger.info("patient.updated", {"id": dto.patient_id})
        return Result(True, "updated")