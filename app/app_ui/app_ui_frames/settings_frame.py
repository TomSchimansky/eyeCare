import customtkinter

from ..app_ui_frames.single_setting_frame_slider import SingleSettingFrameSlider


class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master, app=None, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, master, *args, **kwargs)

        self.app_pointer = app

        self.scroll_delta = 0
        self.max_scrolling = 0

        self.focus_set()

        self.volume_setting_height = 25
        self.volume_setting = SingleSettingFrameSlider(master=self,
                                                       app=self.app_pointer,
                                                       width=350,
                                                       height=50,
                                                       text="Volume",
                                                       callback_function=self.volume_setting_callback)
        self.volume_setting.place(relx=0.5, y=self.volume_setting_height, anchor=customtkinter.N)

        self.time_setting_height = 100
        self.time_setting = SingleSettingFrameSlider(master=self,
                                                     app=self.app_pointer,
                                                     width=350,
                                                     height=50,
                                                     text="Max. Blink Interval",
                                                     callback_function=self.time_setting_callback)
        self.time_setting.place(relx=0.5, y=self.time_setting_height, anchor=customtkinter.N)

        self.bind_tree(self, "<MouseWheel>", self.mouse_wheel_event)

    def bind_tree(self, widget, event, callback):
        """Binds an event to a widget and all its descendants. credits: JAB (stackoverflow.com)"""

        widget.bind(event, callback)
        for child in widget.children.values():
            self.bind_tree(child, event, callback)

    def volume_setting_callback(self, value):
        self.volume_setting.slider_text.configure(text="{}%".format(round(value*100)))
        self.app_pointer.volume_setting = value

    def time_setting_callback(self, value):
        self.time_setting.slider_text.configure(text="{} sec.".format(round(value*30)))
        self.app_pointer.max_time_setting = round(value*30)

    def set_volume_setting(self, value):
        self.volume_setting.slider.set(value)
        self.volume_setting.slider_text.configure(text="{}%".format(round(value * 100)))

    def set_time_setting(self, value):
        self.time_setting.slider.set(value / 30)
        self.time_setting.slider_text.configure(text="{} sec.".format(round(value)))

    def mouse_wheel_event(self, event):
        self.scroll_delta += (event.delta*3)

        if self.scroll_delta <= 0 and self.scroll_delta >= -self.max_scrolling:
            self.volume_setting.place(y=self.volume_setting_height + self.scroll_delta)
            self.time_setting.place(y=self.time_setting_height + self.scroll_delta)

        else:
            self.scroll_delta -= (event.delta*3)
