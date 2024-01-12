

class CTkColorManager:
    MAIN = ("#358ADE", "#166CC1")
    MAIN_HOVER = ("#72AFE8", "#479BEA")
    ENTRY = ("white", "#222222")
    TEXT = ("black", "white")
    SLIDER_BG = ("#6B6B6B", "#222222")
    PROGRESS_BG = ("#6B6B6B", "#222222")
    FRAME = ("#D4D5D6", "#3F3F3F")
    FRAME_2 = ("#C5C5C5", "#505050")

    @classmethod
    def set_theme_color(cls, hex_color, hex_color_hover):
        cls.MAIN = (hex_color, hex_color)
        cls.MAIN_HOVER = (hex_color_hover, hex_color_hover)

    @classmethod
    def set_theme(cls, main_color):
        if main_color.lower() == "green":
            cls.set_theme_color("#2EDEA4", "#82FCD4")

        elif main_color.lower() == "blue":
            cls.set_theme_color("#1C94CF", "#5FB4DD")
