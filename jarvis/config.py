"""Configuration loaded from environment variables and an optional .env file."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Runtime settings for JARVIS."""

    wake_word: str = "jarvis"
    language: str = "en-US"
    picovoice_access_key: str | None = None
    notes_file: Path = Path("data/notes.md")

    @classmethod
    def load(cls) -> "Settings":
        load_dotenv()
        notes_file = Path(os.getenv("JARVIS_NOTES_FILE", "data/notes.md"))
        return cls(
            wake_word=os.getenv("JARVIS_WAKE_WORD", "jarvis").strip().lower(),
            language=os.getenv("JARVIS_LANGUAGE", "en-US"),
            picovoice_access_key=os.getenv("PICOVOICE_ACCESS_KEY") or None,
            notes_file=notes_file,
        )
