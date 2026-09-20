"""Optional speech input/output adapters.

The imports are intentionally lazy so text mode works without microphone
drivers or platform-specific audio libraries installed.
"""

from __future__ import annotations

from dataclasses import dataclass


class SpeechUnavailable(RuntimeError):
    """Raised when voice dependencies or an audio device are unavailable."""


@dataclass
class Speaker:
    """Speak responses aloud when pyttsx3 is available, while always printing."""

    enabled: bool = True

    def say(self, text: str) -> None:
        print(f"JARVIS: {text}")
        if not self.enabled:
            return
        try:
            import pyttsx3

            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception:
            return


class MicrophoneRecognizer:
    """Transcribe one microphone utterance using SpeechRecognition."""

    def __init__(self, language: str = "en-US") -> None:
        self.language = language

    def listen(self) -> str:
        try:
            import speech_recognition as sr
        except ImportError as exc:
            raise SpeechUnavailable(
                "Voice mode needs the optional dependencies. Install with "
                "pip install -e '.[voice]'."
            ) from exc

        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.35)
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=12)
            return recognizer.recognize_google(audio, language=self.language)
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except OSError as exc:
            raise SpeechUnavailable(f"Could not open a microphone: {exc}") from exc
