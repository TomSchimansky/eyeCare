import tkinter
import customtkinter
import time

from app_ui_frames.main_frame import MainFrame

from settings import Settings


class MainView(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        tkinter.Frame.__init__(self, master, *args, **kwargs)

        self.app_pointer = master
        self.color_manager = master.color_manager

        self.settings_button = customtkinter.CTkButton(master=self,
                                                       text="Einstellungen",
                                                       command=lambda: self.app_pointer.show_view("SettingsView"))
        self.settings_button.place(relx=0.05, rely=0.05, anchor=tkinter.NW)

        self.info_button = customtkinter.CTkButton(master=self,
                                                   text="Informationen",
                                                   command=lambda: self.app_pointer.show_view("InfoView"))
        self.info_button.place(relx=0.05, rely=0.17, anchor=tkinter.NW)

        self.about_button = customtkinter.CTkButton(master=self,
                                                    text="Über EyeCare",
                                                    command=self.app_pointer.about_dialog)
        self.about_button.place(relx=0.05, rely=0.29, anchor=tkinter.NW)

        self.main_frame = MainFrame(master=self,
                                    app=self.app_pointer,
                                    width=400,
                                    height=300,
                                    corner_radius=10)
        self.main_frame.place(relx=0.95, rely=0.05, anchor=tkinter.NE)

    def update_eye_analyzer_data(self):
        time_of_last_blink = self.app_pointer.eye_analyzer.time_of_last_blink

        if time_of_last_blink is None:
            self.main_frame.set_eyes_closed()
            self.main_frame.time_bar.set(1)
            self.app_pointer.sound_thread.set_volume(0)

        else:
            time_since_lat_blink = time.time() - time_of_last_blink

            if time_since_lat_blink < self.app_pointer.max_time_setting:
                self.main_frame.set_eyes_open()
                self.main_frame.time_bar.set(1 - (time_since_lat_blink/self.app_pointer.max_time_setting))
                self.app_pointer.sound_thread.set_volume(0)
            elif time_since_lat_blink > self.app_pointer.max_time_setting:
                self.main_frame.set_eyes_open()
                self.main_frame.time_bar.set(0)
                self.app_pointer.sound_thread.set_volume(self.app_pointer.volume_setting)
