from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class RegisterPatientDTO:
    name: str
    email: str
    phone: str | None = None