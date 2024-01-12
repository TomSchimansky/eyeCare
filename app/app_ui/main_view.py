import tkinter
import customtkinter
import time

from .app_ui_frames import MainFrame


class MainView(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        tkinter.Frame.__init__(self, master, *args, **kwargs)

        self.app_pointer = master
        self.color_manager = master.color_manager

        self.settings_button = customtkinter.CTkButton(master=self,
                                                       text="Settings",
                                                       command=lambda: self.app_pointer.show_view("SettingsView"))
        self.settings_button.place(relx=0.05, rely=0.05, anchor=tkinter.NW)

        self.info_button = customtkinter.CTkButton(master=self,
                                                   text="Information",
                                                   command=lambda: self.app_pointer.show_view("InfoView"))
        self.info_button.place(relx=0.05, rely=0.17, anchor=tkinter.NW)

        self.about_button = customtkinter.CTkButton(master=self,
                                                    text="About eyeCare",
                                                    command=self.app_pointer.about_dialog)
        self.about_button.place(relx=0.05, rely=0.29, anchor=tkinter.NW)

        self.main_frame = MainFrame(master=self,
                                    app=self.app_pointer,
                                    width=400,
                                    height=300,
                                    corner_radius=10)
        self.main_frame.place(relx=0.95, rely=0.05, anchor=tkinter.NE)
