import ctypes
import subprocess
import sys
from tkinter import messagebox


def is_admin():
    """Return whether the current process has administrator privileges."""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin(app_name):
    """Request administrator privileges and restart the application."""
    params = subprocess.list2cmdline(sys.argv)

    result = ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        params,
        None,
        1,
    )

    if result <= 32:
        messagebox.showerror(
            app_name,
            "TunnelShare could not restart with administrator "
            "privileges.\n\n"
            "Please run the application as an administrator.",
        )

    sys.exit()