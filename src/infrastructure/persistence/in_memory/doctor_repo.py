from __future__ import annotations
from typing import Dict
from uuid import uuid4
from src.domain.contracts.repositories import DoctorRepository
from src.domain.entities.doctor import Doctor
from src.domain.entities.value_objects import DoctorId


class InMemoryDoctorRepository(DoctorRepository):
    def __init__(self) -> None:
        self._db: Dict[DoctorId, Doctor] = {}

    def next_id(self) -> DoctorId:
        return uuid4()

    def save(self, doctor: Doctor) -> None:
        self._db[doctor.id] = doctor

    def find_by_id(self, did: DoctorId) -> Doctor | None:
        return self._db.get(did)