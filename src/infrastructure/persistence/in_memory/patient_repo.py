from __future__ import annotations
from typing import Dict
from uuid import uuid4
from src.domain.contracts.repositories import PatientRepository
from src.domain.entities.patient import Patient
from src.domain.entities.value_objects import PatientId


class InMemoryPatientRepository(PatientRepository):
    def __init__(self) -> None:
        self._db: Dict[PatientId, Patient] = {}

    def next_id(self) -> PatientId: return uuid4()
    def save(self, patient: Patient) -> None: self._db[patient.id] = patient
    def find_by_id(self, pid: PatientId) -> Patient | None: return self._db.get(pid)
    def find_by_email(self, email: str) -> Patient | None:
        return next((p for p in self._db.values() if p.email == email), None)