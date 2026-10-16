import ctypes
import sys
import traceback


def excepthook(exc_type, exc_value, exc_tb, app_name):
    """Display unexpected errors in a Windows message box."""
    message = "".join(
        traceback.format_exception(exc_type, exc_value, exc_tb)
    )

    try:
        ctypes.windll.user32.MessageBoxW(
            0,
            message,
            f"{app_name} - Unexpected error",
            0x10,
        )
    except Exception:
        pass


def install_exception_handler(app_name):
    """Install a global handler for unexpected exceptions."""

    def handle_exception(exc_type, exc_value, exc_tb):
        excepthook(
            exc_type,
            exc_value,
            exc_tb,
            app_name,
        )

    sys.excepthook = handle_exception