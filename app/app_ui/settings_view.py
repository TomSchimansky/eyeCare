import customtkinter

from app.app_ui.app_ui_frames import SettingsFrame


class SettingsView(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, master, *args, **kwargs)
        self.app_pointer = master

        # configure grid (2x4)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_rowconfigure(3, weight=1)

        self.return_button = customtkinter.CTkButton(master=self,
                                                     text="back",
                                                     command=lambda: self.app_pointer.show_view("MainView"))
        self.return_button.grid(row=0, column=0, padx=(10, 0), pady=(10, 10))

        self.scroll_settings_frame = SettingsFrame(master=self,
                                                   app=self.app_pointer,
                                                   width=400,
                                                   height=300,
                                                   corner_radius=10)
        self.scroll_settings_frame.grid(row=0, column=1, rowspan=4, padx=(10, 10), pady=(10, 10), sticky="nsew")