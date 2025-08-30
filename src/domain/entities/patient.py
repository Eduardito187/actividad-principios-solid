from __future__ import annotations
from dataclasses import dataclass
from .value_objects import PatientId, PhoneNumber, EmailAddress

@dataclass
class Patient:
    id: PatientId
    name: str
    phone: PhoneNumber
    email: EmailAddress