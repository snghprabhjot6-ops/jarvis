"""Small command router and built-in skills."""

from __future__ import annotations

import re
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable
from urllib.parse import quote_plus


@dataclass(frozen=True)
class CommandResult:
    response: str
    should_exit: bool = False


Handler = Callable[[str], CommandResult]


class CommandRouter:
    """Route natural-language-ish text to simple, inspectable skills."""

    def __init__(self) -> None:
        self._handlers: list[tuple[re.Pattern[str], str, Handler]] = []

    def register(self, pattern: str, description: str, handler: Handler) -> None:
        self._handlers.append((re.compile(pattern, re.IGNORECASE), description, handler))

    def descriptions(self) -> list[str]:
        return [description for _, description, _ in self._handlers]

    def dispatch(self, command: str) -> CommandResult:
        cleaned = command.strip()
        for pattern, _, handler in self._handlers:
            match = pattern.fullmatch(cleaned)
            if match:
                return handler(match.groupdict().get("value", "").strip())
        return CommandResult(
            "I heard you, but I do not have a skill for that yet. "
            "Say 'help' to see what I can do."
        )


def build_router(notes_file: Path) -> CommandRouter:
    router = CommandRouter()

    router.register(r"(?:help|what can you do)", "help — list available skills", lambda _: CommandResult(
        "Available skills: " + "; ".join(router.descriptions())
    ))
    router.register(
        r"(?:what is )?the time",
        "time — tell the current local time",
        lambda _: CommandResult(datetime.now().strftime("It is %I:%M %p.")),
    )
    router.register(
        r"(?:what is )?the date|what day is it",
        "date — tell today's date",
        lambda _: CommandResult(datetime.now().strftime("Today is %A, %B %d, %Y.")),
    )
    router.register(
        r"(?:open|visit) (?P<value>.+)",
        "open <site> — open a website in the default browser",
        lambda value: _open_site(value),
    )
    router.register(
        r"(?:search for|google) (?P<value>.+)",
        "search for <query> — search the web",
        lambda value: _search_web(value),
    )
    router.register(
        r"(?:take a )?note(?: that)? (?P<value>.+)",
        "note <text> — save a local note",
        lambda value: _save_note(notes_file, value),
    )
    router.register(
        r"(?:exit|quit|goodbye|shutdown)",
        "exit — stop JARVIS",
        lambda _: CommandResult("Goodbye.", should_exit=True),
    )
    return router


def _open_site(value: str) -> CommandResult:
    target = value.strip()
    if not re.match(r"^https?://", target, re.IGNORECASE):
        target = f"https://{target}"
    webbrowser.open(target)
    return CommandResult(f"Opening {target}.")


def _search_web(value: str) -> CommandResult:
    query = value.strip()
    webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")
    return CommandResult(f"Searching for {query}.")


def _save_note(notes_file: Path, value: str) -> CommandResult:
    notes_file.parent.mkdir(parents=True, exist_ok=True)
    with notes_file.open("a", encoding="utf-8") as handle:
        handle.write(f"- {datetime.now().isoformat(timespec='minutes')}: {value}\n")
    return CommandResult("Saved that note.")
