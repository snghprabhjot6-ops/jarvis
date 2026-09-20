"""Cross-platform system information that does not modify the machine."""

from __future__ import annotations

import getpass
import platform
import shutil
import socket


def status() -> str:
    """Return a short, human-readable system summary."""

    computer = socket.gethostname() or "unknown computer"
    user = getpass.getuser() or "unknown user"
    system = f"{platform.system()} {platform.release()}"
    python = platform.python_version()
    disk = shutil.disk_usage(".")
    free_gb = disk.free / (1024**3)
    return (
        f"You are running JARVIS on {computer} as {user}. "
        f"The system is {system}, Python is {python}, and approximately "
        f"{free_gb:.1f} GB is available."
    )
