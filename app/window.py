import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from app.ics import configure_ics, list_connections
from app.theme import APP_NAME, APP_SUBTITLE, COLORS


class TunnelShareApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("620x470")
        self.resizable(False, False)

        self.center_window()
        self.configure(fg_color=COLORS["background"])

        self.source_var = tk.StringVar()
        self.target_var = tk.StringVar()

        self.connections = []

        self._build_window()
        self.refresh()

    def _configure_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)

    def center_window(self):
        self.update_idletasks()

        width = 620
        height = 470

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_window(self):
        self._configure_window()

        self._build_header()
        self._build_connection_panel()
        self._build_actions()
        self._build_status_bar()

    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        header.grid(
            row=0,
            column=0,
            padx=24,
            pady=(24, 20),
            sticky="ew",
        )

        header.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            header,
            text=APP_NAME,
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
            text_color=COLORS["text"],
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
        )

        subtitle = ctk.CTkLabel(
            header,
            text=APP_SUBTITLE,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["muted"],
        )
        subtitle.grid(
            row=1,
            column=0,
            pady=(4, 0),
            sticky="w",
        )

    def _build_connection_panel(self):
        panel = ctk.CTkFrame(
            self,
            fg_color=COLORS["surface"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        panel.grid(
            row=1,
            column=0,
            padx=24,
            pady=(0, 16),
            sticky="ew",
        )

        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel,
            text="Connection Settings",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
            text_color=COLORS["text"],
        ).grid(
            row=0,
            column=0,
            padx=18,
            pady=(18, 16),
            sticky="w",
        )

        ctk.CTkLabel(
            panel,
            text="Source connection (VPN)",
            text_color=COLORS["muted"],
        ).grid(
            row=1,
            column=0,
            padx=18,
            pady=(0, 6),
            sticky="w",
        )

        self.source_combo = ctk.CTkComboBox(
            panel,
            variable=self.source_var,
            values=[],
            state="readonly",
            height=36,
            corner_radius=8,
            border_color=COLORS["border"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
        )
        self.source_combo.grid(
            row=2,
            column=0,
            padx=18,
            pady=(0, 16),
            sticky="ew",
        )

        ctk.CTkLabel(
            panel,
            text="Target connection (Hotspot)",
            text_color=COLORS["muted"],
        ).grid(
            row=3,
            column=0,
            padx=18,
            pady=(0, 6),
            sticky="w",
        )

        self.target_combo = ctk.CTkComboBox(
            panel,
            variable=self.target_var,
            values=[],
            state="readonly",
            height=36,
            corner_radius=8,
            border_color=COLORS["border"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
        )
        self.target_combo.grid(
            row=4,
            column=0,
            padx=18,
            pady=(0, 18),
            sticky="ew",
        )

    def _build_actions(self):
        actions = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        actions.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 16),
            sticky="ew",
        )

        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

        self.refresh_button = ctk.CTkButton(
            actions,
            text="Refresh Connections",
            command=self.refresh,
            height=40,
            corner_radius=8,
            fg_color=COLORS["surface"],
            hover_color=COLORS["surface_hover"],
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text"],
        )
        self.refresh_button.grid(
            row=0,
            column=0,
            padx=(0, 8),
            sticky="ew",
        )

        self.apply_button = ctk.CTkButton(
            actions,
            text="Enable Sharing",
            command=self.apply,
            height=40,
            corner_radius=8,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color=COLORS["text"],
        )
        self.apply_button.grid(
            row=0,
            column=1,
            padx=(8, 0),
            sticky="ew",
        )

    def _build_status_bar(self):
        status_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["background"],
            corner_radius=8,
            border_width=0,
            border_color=COLORS["background"],
        )
        status_frame.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 20),
            sticky="ew",
        )

        status_frame.grid_columnconfigure(1, weight=1)

        self.status_indicator = ctk.CTkLabel(
            status_frame,
            text="●",
            font=ctk.CTkFont(size=14),
            text_color=COLORS["muted"],
        )
        self.status_indicator.grid(
            row=0,
            column=0,
            padx=(12, 8),
            pady=10,
        )

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            text_color=COLORS["muted"],
            anchor="w",
        )
        self.status_label.grid(
            row=0,
            column=1,
            pady=10,
            sticky="ew",
        )

        self.connection_count_label = ctk.CTkLabel(
            status_frame,
            text="0 connections",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=11),
        )
        self.connection_count_label.grid(
            row=0,
            column=2,
            padx=12,
            pady=10,
        )

    def set_status(self, message, status="info"):
        status_colors = {
            "info": COLORS["muted"],
            "success": COLORS["success"],
            "warning": COLORS["warning"],
            "error": COLORS["error"],
        }

        color = status_colors.get(
            status,
            COLORS["muted"],
        )

        self.status_indicator.configure(
            text_color=color,
        )
        self.status_label.configure(
            text=message,
            text_color=color,
        )

    @staticmethod
    def find_candidate(connections, keywords):
        for connection in connections:
            connection_lower = connection.casefold()

            if any(
                keyword.casefold() in connection_lower
                for keyword in keywords
            ):
                return connection

        return ""

    def refresh(self):
        self.refresh_button.configure(
            state="disabled",
        )
        self.apply_button.configure(
            state="disabled",
        )

        try:
            self.connections = list_connections()

        except Exception as error:
            self.connections = []

            self.source_combo.configure(values=[])
            self.target_combo.configure(values=[])

            self.source_var.set("")
            self.target_var.set("")

            self.connection_count_label.configure(
                text="0 connections",
            )

            self.set_status(
                "Could not load network connections",
                "error",
            )

            messagebox.showerror(
                APP_NAME,
                "Could not retrieve network connections.\n\n"
                f"Error: {error}",
                parent=self,
            )

            return

        self.source_combo.configure(
            values=self.connections,
        )
        self.target_combo.configure(
            values=self.connections,
        )

        if self.source_var.get() not in self.connections:
            source_candidate = self.find_candidate(
                self.connections,
                ["TAP", "Proton", "VPN"],
            )
            self.source_var.set(source_candidate)

        if self.target_var.get() not in self.connections:
            target_candidate = self.find_candidate(
                self.connections,
                ["Local Area Connection*"],
            )
            self.target_var.set(target_candidate)

        self.connection_count_label.configure(
            text=f"{len(self.connections)} connections",
        )

        if self.connections:
            self.set_status(
                "Network connections loaded",
                "success",
            )
        else:
            self.set_status(
                "No network connections found",
                "warning",
            )

        self.refresh_button.configure(
            state="normal",
        )
        self.apply_button.configure(
            state="normal",
        )

    def apply(self):
        source_name = self.source_var.get()
        target_name = self.target_var.get()

        if not source_name or not target_name:
            messagebox.showwarning(
                APP_NAME,
                "Select both the VPN and hotspot connections.",
                parent=self,
            )
            return

        if source_name == target_name:
            messagebox.showwarning(
                APP_NAME,
                "The source and target connections must be different.",
                parent=self,
            )
            return

        confirmed = messagebox.askyesno(
            APP_NAME,
            "Configure Internet Connection Sharing with these "
            "connections?\n\n"
            f"Source (VPN): {source_name}\n"
            f"Target (Hotspot): {target_name}\n\n"
            "Existing Internet Connection Sharing settings may "
            "be changed.",
            parent=self,
        )

        if not confirmed:
            return

        self.refresh_button.configure(
            state="disabled",
        )
        self.apply_button.configure(
            state="disabled",
        )

        self.set_status(
            "Configuring Internet Connection Sharing...",
            "warning",
        )

        try:
            configure_ics(
                source_name,
                target_name,
            )

        except Exception as error:
            error_message = str(error)

            if "could not be fully restored" in error_message.casefold():
                self.set_status(
                    "Configuration failed; restoration incomplete",
                    "error",
                )
            elif (
                "previous sharing configuration was restored"
                in error_message.casefold()
            ):
                self.set_status(
                    "Configuration failed; previous settings restored",
                    "error",
                )
            else:
                self.set_status(
                    "Could not configure Internet Connection Sharing",
                    "error",
                )

            messagebox.showerror(
                APP_NAME,
                error_message,
                parent=self,
            )

        else:
            self.set_status(
                "Internet Connection Sharing configured successfully",
                "success",
            )

            messagebox.showinfo(
                APP_NAME,
                "Internet Connection Sharing was configured "
                "successfully.\n\n"
                f"Source (VPN): {source_name}\n"
                f"Target (Hotspot): {target_name}",
                parent=self,
            )

        finally:
            self.refresh_button.configure(
                state="normal",
            )
            self.apply_button.configure(
                state="normal",
            )