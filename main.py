from app.admin import is_admin, relaunch_as_admin
from app.errors import install_exception_handler
from app.theme import APP_NAME
from app.window import TunnelShareApp


if __name__ == "__main__":
    install_exception_handler(APP_NAME)

    if not is_admin():
        relaunch_as_admin(APP_NAME)

    app = TunnelShareApp()
    app.mainloop()