import tkinter
import tkinter.messagebox
import customtkinter
import sys
import json
from settings import Settings

from app_analyzing.timing import Timer

from app_ui_views.start_view import StartView
from app_ui_views.loading_view import LoadingView
from app_ui_views.main_view import MainView
from app_ui_views.settings_view import SettingsView
from app_ui_views.info_view import InfoView

from app_analyzing.eye_analyzer import EyeAnalyzer
from app_analyzing.sound_thread import SoundThread


class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        customtkinter.enable_macos_darkmode()
        customtkinter.deactivate_threading()
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.color_manager = None

        self.minsize(Settings.MIN_WIDTH, Settings.MIN_HEIGHT)
        self.maxsize(Settings.MAX_WIDTH, Settings.MAX_HEIGHT)
        self.resizable(False, False)
        self.title(Settings.APP_NAME)
        self.geometry(str(Settings.DEFAULT_WIDTH) + "x" + str(Settings.DEFAULT_HEIGHT))

        if sys.platform == "darwin":  # macOS
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)

        elif "win" in sys.platform:  # Windows
            self.bind("<Alt-Key-F4>", self.on_closing)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        if sys.platform == "darwin":  # macOS
            self.menubar = tkinter.Menu(master=self)
            self.app_menu = tkinter.Menu(self.menubar, name='apple')
            self.menubar.add_cascade(menu=self.app_menu)

            self.app_menu.add_command(label='About ' + Settings.APP_NAME, command=self.about_dialog)
            self.app_menu.add_separator()

            self.config(menu=self.menubar)
            self.createcommand('tk::mac::Quit', self.on_closing)

        self.running = False

        self.main_view = MainView(self)
        self.loading_view_start = LoadingView(self,
                                              call_when_ready=lambda: self.show_view("MainView"))
        self.start_view = StartView(self)
        self.settings_view = SettingsView(self)
        self.info_view = InfoView(self)

        self.views = []
        self.views.append(self.main_view)
        self.views.append(self.loading_view_start)
        self.views.append(self.start_view)
        self.views.append(self.settings_view)
        self.views.append(self.info_view)

        self.eye_analyzer = EyeAnalyzer()
        self.sound_thread = SoundThread()
        self.sound_thread.start()

        self.timer = Timer(Settings.FPS)

        self.volume_setting = 0.5  # percent
        self.max_time_setting = 5  # secs

    def read_user_settings_from_file(self):
        with open(Settings.USER_SETTINGS_PATH, "r") as file:
            user_settings = json.load(file)

        self.volume_setting = user_settings["volume_setting"]
        self.max_time_setting = user_settings["max_time_setting"]

    def write_user_settings_to_file(self):
        user_settings = {"volume_setting": self.volume_setting,
                         "max_time_setting": self.max_time_setting}

        with open(Settings.USER_SETTINGS_PATH, "w") as file:
            json.dump(user_settings, file)

    def start_analyzing(self):
        self.eye_analyzer.activate_analyzing()

    def stop_analyzing(self):
        self.eye_analyzer.deactivate_analyzing()

    def show_view(self, view_name):
        """ Draw specified view (class-name) and hide all other """

        for view in self.views:
            if view_name.lower() == view.__class__.__name__.lower():
                view.place(relx=0, rely=0, relheight=1, relwidth=1)
            else:
                view.place_forget()

    @staticmethod
    def about_dialog():
        tkinter.messagebox.showinfo(title=Settings.APP_NAME,
                                    message=Settings.ABOUT_TEXT)

    def on_closing(self, event=0):
        self.write_user_settings_to_file()
        customtkinter.disable_macos_darkmode()
        self.eye_analyzer.stop()
        self.running = False

    def start(self):
        self.running = True

        # load settings
        self.read_user_settings_from_file()
        self.settings_view.scroll_settings_frame.set_volume_setting(self.volume_setting)
        self.settings_view.scroll_settings_frame.set_time_setting(self.max_time_setting)

        self.show_view("LoadingView")
        self.eye_analyzer.start()
        self.eye_analyzer.start_loading()

        while self.running:

            if self.loading_view_start.get_loading_status() < 1:
                self.loading_view_start.set_loading_status(self.eye_analyzer.loading_status)
            else:
                self.main_view.main_frame.update_info_data(self.eye_analyzer.get_average_blink_time())
                self.main_view.update_eye_analyzer_data()

            self.update()
            customtkinter.update_theme()
            self.timer.wait()

        self.destroy()


if __name__ == "__main__":
    app = App()
    app.start()
