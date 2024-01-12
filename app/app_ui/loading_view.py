import tkinter
import customtkinter


class LoadingView(tkinter.Frame):
    def __init__(self, master, call_when_ready=None, *args, **kwargs):
        tkinter.Frame.__init__(self, master, *args, **kwargs)

        self.app_pointer = master
        self.color_manager = master.color_manager

        self.callback_function = call_when_ready

        self.progress = 0

        self.loading_bar = customtkinter.CTkProgressBar(master=self,
                                                        width=300,
                                                        height=20,
                                                        border_width=1)
        self.loading_bar.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.loading_bar.set(0)

    def set_loading_status(self, progress):
        self.progress = progress
        self.loading_bar.set(self.progress)

        if self.progress == 1:
            if self.callback_function is not None:
                self.callback_function()

    def get_loading_status(self):
        return self.progress