import customtkinter

from settings import Settings


class InfoView(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, master, *args, **kwargs)

        self.app_pointer = master

        self.return_button = customtkinter.CTkButton(master=self,
                                                     text="back",
                                                     command=lambda: self.app_pointer.show_view("MainView"))
        self.return_button.place(relx=0.05, rely=0.05, anchor=customtkinter.NW)

        self.text_frame = customtkinter.CTkFrame(master=self,
                                                 width=400,
                                                 height=300,
                                                 corner_radius=10)
        self.text_frame.place(relx=0.95, rely=0.05, anchor=customtkinter.NE)

        self.welcome_text = customtkinter.CTkLabel(master=self.text_frame,
                                                   width=350,
                                                   height=200,
                                                   text=Settings.INFO_TEXT)
        self.welcome_text.place(relx=0.5, rely=0.1, anchor=customtkinter.N)