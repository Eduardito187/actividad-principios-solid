from __future__ import annotations
from src.infrastructure.logging.std_logger import LoggedValueError
from src.domain.contracts.notification import NotificationChannel
from src.shared.validators import is_valid_email

class EmailChannel(NotificationChannel):
    def __init__(self, mailer: object | None = None) -> None:
        self._mailer = mailer

    def send(self, to, subject: str, message: str) -> None:
        if to.email == None:
            return
        if not is_valid_email(to.email.value):
            raise LoggedValueError("Email inválido")
        print(f"[EMAIL] to={to.email.value} :: {subject} :: {message}")