from .customtkinter_button import CTkButton
from .customtkinter_slider import CTkSlider
from .customtkinter_frame import CTkFrame
from .customtkinter_progressbar import CTkProgressBar
from .customtkinter_label import CTkLabel
from .customtkinter_entry import CTkEntry
from .appearance_mode_tracker import AppearanceModeTracker, SystemAppearanceModeListenerNoThread
from .customtkinter_color_manager import CTkColorManager as Color

import sys


def set_appearance_mode(mode_string):
    AppearanceModeTracker.set_appearance_mode(mode_string)


def get_appearance_mode():
    if AppearanceModeTracker.appearance_mode == 0:
        return "Light"
    elif AppearanceModeTracker.appearance_mode == 1:
        return "Dark"


def set_theme(main_color):
    Color.set_theme(main_color)


def deactivate_threading():
    AppearanceModeTracker.init_listener_function(no_thread=True)
    sys.stderr.write("WARNING (customtkinter.deactivate_threading): Automatic threaded search for a change of the " +
                     "system appearance mode is deativated now.\nYou have to update the appearance mode manually " +
                     "in your mainloop by calling customtkinter.update_theme().\n")


def activate_threading():
    AppearanceModeTracker.init_listener_function()


def update_theme():
    if isinstance(AppearanceModeTracker.system_mode_listener, SystemAppearanceModeListenerNoThread):
        AppearanceModeTracker.system_mode_listener.update()
    else:
        sys.stderr.write("WARNING (customtkinter.update_theme): no need to call update_theme, because " +
                         "customtkinter is constantly searching for a mode change in a background thread.\n")






