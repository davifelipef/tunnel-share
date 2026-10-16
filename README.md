# TunnelShare

**A lightweight Windows utility for sharing a VPN connection over a mobile hotspot.**

TunnelShare simplifies the configuration of Windows Internet Connection Sharing (ICS), allowing you to share your VPN connection with devices connected to your computer's hotspot.

Instead of navigating through Windows network settings manually, TunnelShare provides a simple graphical interface to select the source and target network connections and configure sharing.

## Features

- **Simple graphical interface** — Manage network sharing through a clean, dark-themed interface.
- **VPN-to-hotspot sharing** — Share a VPN connection with devices connected to your Windows hotspot.
- **Automatic connection discovery** — Detect available network connections and suggest likely VPN and hotspot interfaces.
- **Administrator privileges** — Request elevated permissions when required.
- **Configuration recovery** — Attempt to restore the previous Internet Connection Sharing configuration if an operation fails.
- **Connection status** — Display the current operation status and the number of detected network connections.
- **Lightweight implementation** — Built with Python and CustomTkinter, using Windows' native Internet Connection Sharing functionality.

## Requirements

- Windows with Internet Connection Sharing (ICS) support.
- Python 3.10 or later.
- Administrator privileges.
- A VPN connection.
- A Windows mobile hotspot or another network interface to receive the shared connection.

### Dependencies

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — Modern graphical user interface.
- [pywin32](https://github.com/mhammond/pywin32) — Access to Windows COM interfaces used to configure Internet Connection Sharing.

## Installation

### 1. Clone the repository

```bash
git clone <https://github.com/davifelipef/tunnel-share.git>
cd TunnelShare
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Or in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install customtkinter pywin32
```

### 4. Run the application

```bash
python main.py
```

TunnelShare will request administrator privileges if it is not already running with elevation.

## Usage

1. Connect to your VPN.
2. Enable the Windows mobile hotspot.
3. Launch TunnelShare.
4. Select your VPN interface under **Source connection**.
5. Select your hotspot interface under **Target connection**.
6. Click **Enable Sharing**.
7. Review the selected connections and confirm the operation.

TunnelShare will configure Internet Connection Sharing, setting the VPN interface as the public connection and the hotspot interface as the private connection.

Use **Refresh Connections** to reload the available network interfaces.

## How It Works

TunnelShare uses Windows' native Internet Connection Sharing functionality through the `HNetCfg.HNetShare` COM interface.

The application configures two network roles:

| Role             | Description                                                                    |
| ---------------- | ------------------------------------------------------------------------------ |
| Source (Public)  | The VPN connection that provides Internet access.                              |
| Target (Private) | The hotspot interface that distributes the shared connection to other devices. |

Before applying a new configuration, TunnelShare records the existing enabled sharing connections. If the operation fails, it attempts to restore the previous configuration.

Restoration is best-effort: Windows may prevent some changes from being reversed, so a failed operation can require manual inspection of the ICS settings.

## Project Structure

```text
TunnelShare/
├── main.py
├── README.md
├── requirements.txt
└── app/
    ├── __init__.py
    ├── admin.py
    ├── errors.py
    ├── ics.py
    ├── theme.py
    └── window.py
```

| File            | Responsibility                                      |
| --------------- | --------------------------------------------------- |
| `main.py`       | Application entry point and startup sequence.       |
| `app/admin.py`  | Administrator privilege detection and elevation.    |
| `app/errors.py` | Global handling of unexpected exceptions.           |
| `app/ics.py`    | Network connection discovery and ICS configuration. |
| `app/theme.py`  | Application name, subtitle, and color palette.      |
| `app/window.py` | Graphical interface and user interactions.          |

## Troubleshooting

### No network connections are displayed

- Click **Refresh Connections**.
- Verify that the VPN and hotspot interfaces are available in Windows.
- Run the application with administrator privileges.

### Internet sharing fails

- Verify that both selected interfaces still exist.
- Ensure that the VPN is connected and the hotspot is enabled.
- Check whether another application or Windows configuration is interfering with ICS.
- Inspect the Windows network adapter sharing settings if the previous configuration could not be restored.

### Connected devices have no Internet access

- Confirm that the VPN is connected.
- Verify that the hotspot is using the intended network interface.
- Check the Windows hotspot and ICS settings.
- Keep in mind that VPN routing policies, firewall rules, and VPN client restrictions can affect connectivity.

## Limitations

- Windows only.
- Requires administrator privileges to configure Internet Connection Sharing.
- Depends on Windows networking services and COM interfaces.
- Automatic interface suggestions are based on connection names and may not identify every VPN or hotspot configuration correctly.
- Restoring a previous configuration is not guaranteed if Windows rejects the restoration operations.
- TunnelShare does not create a VPN connection; it shares an existing one.

## License

No license has been specified yet.

Unless a license is added to the repository, do not assume that the project is released under an open-source license or that others have permission to redistribute or modify it.
