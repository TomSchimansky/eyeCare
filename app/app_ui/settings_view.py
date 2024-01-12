import tkinter
import customtkinter

from app.app_ui.app_ui_frames import SettingsFrame


class SettingsView(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        tkinter.Frame.__init__(self, master, *args, **kwargs)

        self.app_pointer = master
        self.color_manager = master.color_manager

        self.return_button = customtkinter.CTkButton(master=self,
                                                     text="zurück",
                                                     command=lambda: self.app_pointer.show_view("MainView"))
        self.return_button.place(relx=0.05, rely=0.05, anchor=tkinter.NW)

        self.scroll_settings_frame = SettingsFrame(master=self,
                                                   app=self.app_pointer,
                                                   width=400,
                                                   height=300,
                                                   corner_radius=10)
        self.scroll_settings_frame.place(relx=0.95, rely=0.05, anchor=tkinter.NE)