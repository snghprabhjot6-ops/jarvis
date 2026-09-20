"""A tiny JSON-backed reminder store."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path


@dataclass(frozen=True)
class Reminder:
    text: str
    due_at: str
    created_at: str


class ReminderStore:
    """Persist reminders locally so they survive a JARVIS restart."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def add_in_minutes(self, minutes: int, text: str) -> Reminder:
        if minutes < 1 or minutes > 60 * 24 * 365:
            raise ValueError("minutes must be between 1 and 525600")
        now = datetime.now()
        reminder = Reminder(
            text=text,
            due_at=(now + timedelta(minutes=minutes)).isoformat(timespec="minutes"),
            created_at=now.isoformat(timespec="minutes"),
        )
        reminders = self._read()
        reminders.append(reminder)
        self._write(reminders)
        return reminder

    def pending(self) -> list[Reminder]:
        return self._read()

    def clear(self) -> int:
        count = len(self._read())
        if self.path.exists():
            self.path.unlink()
        return count

    def _read(self) -> list[Reminder]:
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        return [Reminder(**item) for item in raw if isinstance(item, dict)]

    def _write(self, reminders: list[Reminder]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps([asdict(item) for item in reminders], indent=2)
        self.path.write_text(payload + "\n", encoding="utf-8")
