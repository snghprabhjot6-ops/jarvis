# JARVIS

JARVIS is a small, extensible personal voice assistant with wake-word activation and a growing set of local skills.

## Included

- Built-in jarvis wake word through Picovoice Porcupine.
- Speech-to-text and spoken responses in voice mode.
- Text mode for development without a microphone or API key.
- Skills for help, time, date, websites, web search, notes, arithmetic, reminders, and system status.
- A top-level main.py launcher for PyCharm.
- Pytest coverage and GitHub Actions CI.

## Quick start

Create a virtual environment, install the project with the test extras, and run:

    python -m jarvis --mode text

You can try:

    jarvis help
    calculate 12 plus 8
    note remember to build a calendar skill
    remind me in 15 minutes to stretch
    show reminders
    system status
    goodbye

## Start with PyCharm

Open the project folder, select the project virtual environment as the interpreter, open main.py, and click Run. Add --mode text or --mode voice in the Run Configuration parameters.

## Voice mode

Install the voice extras with:

    python -m pip install -e .[voice]

Create a Picovoice AccessKey at https://console.picovoice.ai/, copy .env.example to .env, and set PICOVOICE_ACCESS_KEY. Then run:

    python -m jarvis --mode voice

Say Jarvis, wait for the response, and give a command. The default --mode auto selects voice mode when the access key is configured and otherwise opens text mode.

## Skills and project layout

The root main.py is a convenience launcher. The jarvis package contains runtime and speech code. Built-in skill helpers live under jarvis/skills/, while commands.py connects spoken phrases to those skills. Reminders are saved locally in data/reminders.json and notes are saved in data/notes.md.

To add a skill, create a focused helper under jarvis/skills/ and register a command in jarvis/commands.py. Keep secrets in .env; it is ignored by Git. Review new skills before granting them access to files, shell commands, or external services.

## Development

Install the test extras and run:

    pytest

JARVIS is released under the MIT License.
