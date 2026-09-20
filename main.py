"""Convenience launcher for running JARVIS from the project root.

This file makes the project easy to start in PyCharm: open this file and
click Run. The package entry point remains available through python -m jarvis
and the installed jarvis command.
"""

from jarvis.main import main


if __name__ == "__main__":
    raise SystemExit(main())
