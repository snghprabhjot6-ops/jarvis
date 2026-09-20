# JARVIS

JARVIS is a small, extensible personal voice assistant with wake-word activation.

## Included

- Built-in `jarvis` wake word through Picovoice Porcupine.
- Speech-to-text and spoken responses in voice mode.
- Text mode for development without a microphone or API key.
- Skills for help, time, date, opening websites, web search, and local notes.
- Pytest coverage and GitHub Actions CI.

## Quick start

Create a virtual environment, install the project with the test extras, and run `python -m jarvis --mode text`. You can try `jarvis help`, `what is the time`, `note remember to build a calendar skill`, `open github.com`, and `goodbye`.

## Voice mode

Install the voice extras with `python -m pip install -e ".[voice]"`. Create a Picovoice AccessKey at https://console.picovoice.ai/, copy `.env.example` to `.env`, and set `PICOVOICE_ACCESS_KEY`. Then run `python -m jarvis --mode voice`, say `Jarvis`, wait for the response, and give a command.

`--mode auto` selects voice mode when the access key is configured and otherwise opens text mode. Microphone support depends on your operating system audio drivers.

## Adding skills

Register a handler in `jarvis/commands.py`, or add larger capabilities under `jarvis/skills/`. Keep secrets in `.env`; it is ignored by Git. Notes are saved locally to `data/notes.md`. Review new skills before granting them access to files, shell commands, or external services.

## Development

Install the test extras and run `pytest`. JARVIS is released under the MIT License.
