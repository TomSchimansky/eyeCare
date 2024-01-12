import tkinter
import customtkinter

from settings import Settings


class SingleSettingFrameOnOff(customtkinter.CTkFrame):
    def __init__(self, master, app=None, text="", on_text="", off_text="", *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, master, *args, **kwargs)

        self.app_pointer = app
        self.color_manager = master.color_manager
        self.image_manager = master.image_manager
        self.image_manager = master.image_manager

        self.status = "positive"
        self.text = text
        self.on_text = on_text
        self.off_text = off_text

        self.info_text = customtkinter.CTkLabel(master=self,
                                          text=self.text)
        self.info_text.place(relx=0.05, rely=0.5, anchor=tkinter.W)

        self.button = customtkinter.CTkButton(master=self,
                                          text=self.off_text,
                                          command=self.button_press)
        self.button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

    def button_press(self):
        if self.status == "positive":
            self.status = "negative"
            self.button.set_text(self.on_text)
        elif self.status == "negative":
            self.status = "positive"
            self.button.set_text(self.off_text)