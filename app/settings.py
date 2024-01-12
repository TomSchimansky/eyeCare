import os


class Settings:
    MAIN_PATH = os.path.dirname(__file__)

    VERSION = "1.0"
    AUTHOR = "Tom Schimansky"
    
    APP_NAME = "eyeCare"
    ABOUT_TEXT = "Version {}\nby {}".format(VERSION, AUTHOR)
    INFO_TEXT = "This app locates your eyes with\nthe camera and detects when\nyou blink.\n\n" +\
                "The camera images don't get not saved to the\nhard drive or get processed in any other\n" +\
                "way, than running the detection algorithm on them."

    USER_SETTINGS_PATH = MAIN_PATH + "/app_user_settings/user_settings.json"

    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 350

    MIN_WIDTH = DEFAULT_WIDTH
    MIN_HEIGHT = DEFAULT_HEIGHT

    MAX_WIDTH = DEFAULT_WIDTH
    MAX_HEIGHT = DEFAULT_HEIGHT

    FPS = 60
