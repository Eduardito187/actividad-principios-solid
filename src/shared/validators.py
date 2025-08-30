from __future__ import annotations
import re

def is_valid_phone_8d(to: str) -> bool:
    return re.fullmatch(r"\d{8}", to) is not None

def is_valid_email(to: str) -> bool:
    return re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", to) is not None

def normalize_phone_local(to: str) -> str:
    return re.sub(r"[^\d]", "", to)