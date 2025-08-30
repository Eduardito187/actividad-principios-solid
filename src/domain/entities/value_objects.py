from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from src.infrastructure.logging.std_logger import LoggedValueError
import re

PatientId = UUID
DoctorId = UUID
AppointmentId = UUID

@dataclass(frozen=True)
class TimeSlot:
    start: datetime
    end: datetime

    def __post_init__(self):
        if self.end <= self.start:
            raise LoggedValueError("end must be after start")

    def overlaps(self, other: "TimeSlot") -> bool:
        return self.start < other.end and other.start < self.end

@dataclass(frozen=True, slots=True)
class PhoneNumber:
    value: str

    def __post_init__(self):
        normalized = re.sub(r"[^\d]", "", self.value)
        if not re.fullmatch(r"\d{8}", normalized):
            raise LoggedValueError("Teléfono inválido (se esperan 8 dígitos)")
        object.__setattr__(self, "value", normalized)

@dataclass(frozen=True, slots=True)
class EmailAddress:
    value: str

    def __post_init__(self):
        if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", self.value):
            raise LoggedValueError("Email inválido")