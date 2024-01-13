import customtkinter

from .app_ui_frames import MainFrame


class MainView(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, master, *args, **kwargs)
        self.app_pointer = master

        # configure grid (2x4)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_rowconfigure(3, weight=1)

        self.settings_button = customtkinter.CTkButton(master=self,
                                                       text="Settings",
                                                       command=lambda: self.app_pointer.show_view("SettingsView"))
        self.settings_button.grid(row=0, column=0, padx=(10, 0), pady=(10, 10))

        self.info_button = customtkinter.CTkButton(master=self,
                                                   text="Information",
                                                   command=lambda: self.app_pointer.show_view("InfoView"))
        self.info_button.grid(row=1, column=0, padx=(10, 0), pady=(0, 10))

        self.about_button = customtkinter.CTkButton(master=self,
                                                    text="About eyeCare",
                                                    command=self.app_pointer.about_dialog)
        self.about_button.grid(row=2, column=0, padx=(10, 0), pady=(0, 10))

        self.main_frame = MainFrame(master=self,
                                    app=self.app_pointer,
                                    corner_radius=10)
        self.main_frame.grid(row=0, column=1, rowspan=4, padx=(10, 10), pady=(10, 10), sticky="nsew")
