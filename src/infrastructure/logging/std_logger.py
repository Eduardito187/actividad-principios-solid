from __future__ import annotations
from datetime import datetime
from src.domain.contracts.audit import AuditLogger

class StdLogger(AuditLogger):
    LOG_FILE = "info.log"

    def info(self, event: str, context: dict | None = None) -> None:
        with open(self.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] {event} {context or {}}\n")

class LoggedValueError(Exception):
    LOG_FILE = "errors.log"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self._log_to_file()

    def _log_to_file(self):
        with open(self.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] {self.message}\n")
