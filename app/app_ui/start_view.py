import customtkinter

from .app_ui_frames import WelcomeFrame


class StartView(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, master, *args, **kwargs)

        self.app_pointer = master

        self.welcome_frame = WelcomeFrame(master=self,
                                          app=self.app_pointer,
                                          width=350,
                                          height=250,
                                          corner_radius=10)
        self.welcome_frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
