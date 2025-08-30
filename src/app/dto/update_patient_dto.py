from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class UpdatePatientDTO:
    patient_id: str
    name: str | None = None
    email: str | None = None
    phone: str | None = None