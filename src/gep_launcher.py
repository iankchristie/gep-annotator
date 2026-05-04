import os
import subprocess
import sys
import time
from pathlib import Path

from config import TARGET_KML_PATH


# Default Google Earth Pro install locations per platform. Override with the
# GEP_PATH environment variable if you installed it somewhere else.
_DEFAULT_GEP_PATHS = {
    "win32": [
        r"C:\Program Files\Google\Google Earth Pro\client\googleearth.exe",
        r"C:\Program Files (x86)\Google\Google Earth Pro\client\googleearth.exe",
    ],
    "darwin": ["Google Earth Pro"],  # handed to `open -a`, not a filesystem path
    "linux": ["/usr/bin/google-earth-pro", "/opt/google/earth/pro/googleearth"],
}


def _resolve_gep_path() -> str:
    """Return the launcher path/name appropriate for this OS."""
    override = os.environ.get("GEP_PATH")
    if override:
        return override

    candidates = _DEFAULT_GEP_PATHS.get(sys.platform, [])
    for candidate in candidates:
        # On macOS the candidate is an app name, not a file path — always accept it.
        if sys.platform == "darwin":
            return candidate
        if Path(candidate).exists():
            return candidate

    raise FileNotFoundError(
        "Could not find Google Earth Pro. Set the GEP_PATH environment variable "
        "to the full path of the Google Earth Pro executable."
    )


def _open_with_gep(kml_path: str | None = None) -> None:
    """Launch GEP, optionally opening a KML file."""
    gep = _resolve_gep_path()

    if sys.platform == "darwin":
        cmd = ["open", "-a", gep]
        if kml_path is not None:
            cmd.append(kml_path)
        subprocess.Popen(cmd)
    elif sys.platform == "win32":
        args = [gep]
        if kml_path is not None:
            args.append(kml_path)
        # close_fds + DETACHED_PROCESS so GEP isn't tied to our console
        subprocess.Popen(
            args,
            close_fds=True,
            creationflags=getattr(subprocess, "DETACHED_PROCESS", 0),
        )
    else:  # linux and friends
        args = [gep]
        if kml_path is not None:
            args.append(kml_path)
        subprocess.Popen(args, close_fds=True)


def launch_gep() -> None:
    print("Launching Google Earth Pro...")
    _open_with_gep()
    print("Waiting for Google Earth Pro to initialize...")
    time.sleep(5)
    print("Ready.\n")


def open_target_kml() -> None:
    _open_with_gep(str(TARGET_KML_PATH.resolve()))
