import customtkinter


class SingleSettingFrameSlider(customtkinter.CTkFrame):
    def __init__(self, master, app=None, text="", callback_function=None, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, master, *args, **kwargs)

        self.app_pointer = app

        self.text = text
        self.callback_function = callback_function

        self.info_text = customtkinter.CTkLabel(master=self,
                                                text=self.text)
        self.info_text.place(relx=0.05, rely=0.5, anchor=customtkinter.W)

        self.slider = customtkinter.CTkSlider(master=self,
                                              width=150,
                                              height=15,
                                              command=self.slider_callback)
        self.slider.place(relx=0.6, rely=0.5, anchor=customtkinter.CENTER)

        self.slider_text = customtkinter.CTkLabel(master=self,
                                                  width=50,
                                                  text="100%")
        self.slider_text.place(relx=0.9, rely=0.5, anchor=customtkinter.CENTER)

    def slider_callback(self, value):
        if self.callback_function is not None:
            self.callback_function(value)