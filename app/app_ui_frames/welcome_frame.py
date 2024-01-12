import tkinter
import customtkinter

from settings import Settings


class WelcomeFrame(customtkinter.CTkFrame):
    def __init__(self, master, app=None, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, master, *args, **kwargs)

        self.app_pointer = app
        self.color_manager = master.color_manager

        self.button = customtkinter.CTkButton(master=self,
                                              text="Start eyeCare",
                                              command=self.start_loading)
        self.button.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

        self.welcome_text = customtkinter.CTkLabel(master=self,
                                                   width=200,
                                                   height=50,
                                                   text=Settings.INFO_TEXT)
        self.welcome_text.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

    def start_loading(self):
        self.app_pointer.eye_analyzer.start_loading()
        self.app_pointer.show_view("LoadingView")