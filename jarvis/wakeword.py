"""Wake-word listeners."""

from __future__ import annotations

from dataclasses import dataclass

from .config import Settings
from .speech import SpeechUnavailable


@dataclass
class PorcupineWakeWord:
    """Listen continuously for a built-in Porcupine wake word."""

    settings: Settings

    def wait(self) -> None:
        if not self.settings.picovoice_access_key:
            raise SpeechUnavailable(
                "Voice wake-word mode needs PICOVOICE_ACCESS_KEY in .env. "
                "Create a free key at https://console.picovoice.ai/."
            )

        try:
            import pvporcupine
            from pvrecorder import PvRecorder
        except ImportError as exc:
            raise SpeechUnavailable(
                "Wake-word mode needs the optional voice dependencies. "
                "Install with pip install -e '.[voice]'."
            ) from exc

        try:
            porcupine = pvporcupine.create(
                access_key=self.settings.picovoice_access_key,
                keywords=[self.settings.wake_word],
            )
            recorder = PvRecorder(frame_length=porcupine.frame_length, device_index=-1)
            recorder.start()
            print(f"Waiting for the '{self.settings.wake_word}' wake word...")
            while True:
                if porcupine.process(recorder.read()) >= 0:
                    return
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            raise SpeechUnavailable(f"Wake-word listener failed: {exc}") from exc
        finally:
            try:
                recorder.stop()
                recorder.delete()
            except (UnboundLocalError, NameError):
                pass
            try:
                porcupine.delete()
            except (UnboundLocalError, NameError):
                pass
