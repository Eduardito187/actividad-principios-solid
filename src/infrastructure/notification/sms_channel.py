from __future__ import annotations
from src.infrastructure.logging.std_logger import LoggedValueError
from src.domain.contracts.notification import NotificationChannel
from src.shared.validators import is_valid_phone_8d, normalize_phone_local

class SmsChannel(NotificationChannel):
    def __init__(self, sms_client: object | None = None) -> None:
        self._client = sms_client

    def send(self, to, subject: str, message: str) -> None:
        if to.phone == None:
            return
        phone = normalize_phone_local(to.phone.value)
        if not is_valid_phone_8d(phone):
            raise LoggedValueError("Teléfono inválido")
        print(f"[SMS] to={phone} :: {subject} :: {message}")