from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class BookAppointmentDTO:
    patient_id: str
    doctor_id: str
    start: datetime
    end: datetime