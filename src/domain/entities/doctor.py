from __future__ import annotations
from dataclasses import dataclass
from .value_objects import DoctorId, PhoneNumber, EmailAddress
from .specialties import Specialty

@dataclass
class Doctor:
    id: DoctorId
    name: str
    specialty: Specialty
    phone: PhoneNumber|None
    email: EmailAddress|None