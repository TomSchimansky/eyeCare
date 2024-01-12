

class ColorManager(object):
    def __init__(self):
        self.dark_background_layer_1 = self.rgb_to_hex((58, 58, 58))
        self.dark_background_layer_2 = self.rgb_to_hex((19,19,19))
        self.dark_background_layer_3 = self.rgb_to_hex((58, 58, 58))

        self.button_color = self.rgb_to_hex((40, 121, 148))
        self.button_color_hover = self.rgb_to_hex((51, 180, 222))

        self.progress_bar_color_front = self.rgb_to_hex((40, 121, 148))
        self.progress_bar_color_back = self.rgb_to_hex((0, 0, 0))

        self.status_positive = self.rgb_to_hex((180, 0, 20))
        self.status_negative = self.rgb_to_hex((20, 180, 0))

        self.text_color = self.rgb_to_hex((255, 255, 255))

    @staticmethod
    def rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb