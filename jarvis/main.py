"""JARVIS command-line entry point."""

from __future__ import annotations

import argparse
import sys

from .commands import CommandResult, build_router
from .config import Settings
from .speech import MicrophoneRecognizer, Speaker, SpeechUnavailable
from .wakeword import PorcupineWakeWord


def _remove_wake_word(text: str, wake_word: str) -> str | None:
    cleaned = text.strip()
    prefix = wake_word.lower()
    if cleaned.lower() == prefix:
        return ""
    if cleaned.lower().startswith(prefix + " "):
        return cleaned[len(prefix) :].strip()
    return None


def _handle(router, speaker: Speaker, command: str) -> bool:
    result: CommandResult = router.dispatch(command)
    speaker.say(result.response)
    return result.should_exit


def run_text(settings: Settings) -> None:
    router = build_router(settings.notes_file)
    speaker = Speaker(enabled=False)
    print(f"JARVIS text mode. Type '{settings.wake_word} help' or 'help'. Ctrl-C to exit.")
    while True:
        try:
            line = input("You: ").strip()
        except EOFError:
            return
        if not line:
            continue
        command = _remove_wake_word(line, settings.wake_word)
        if command is None:
            command = line
        if not command:
            speaker.say("Yes?")
            continue
        if _handle(router, speaker, command):
            return


def run_voice(settings: Settings) -> None:
    router = build_router(settings.notes_file)
    speaker = Speaker()
    recognizer = MicrophoneRecognizer(settings.language)
    wake_word = PorcupineWakeWord(settings)
    speaker.say("JARVIS is online.")
    while True:
        wake_word.wait()
        speaker.say("Yes?")
        command = recognizer.listen().strip()
        if not command:
            speaker.say("I did not catch that.")
            continue
        if _handle(router, speaker, command):
            return


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run your JARVIS personal assistant.")
    parser.add_argument(
        "--mode",
        choices=("auto", "text", "voice"),
        default="auto",
        help="auto uses voice when PICOVOICE_ACCESS_KEY is configured; otherwise text",
    )
    args = parser.parse_args(argv)
    settings = Settings.load()
    mode = args.mode
    if mode == "auto":
        mode = "voice" if settings.picovoice_access_key else "text"
    try:
        if mode == "voice":
            run_voice(settings)
        else:
            run_text(settings)
    except KeyboardInterrupt:
        print("\nJARVIS offline.")
    except SpeechUnavailable as exc:
        print(f"JARVIS could not start voice mode: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
