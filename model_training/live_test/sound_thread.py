from threading import Thread
from playsound import playsound
import time


class SoundThread(Thread):
    def __init__(self, path_to_file):
        Thread.__init__(self)
        self.running = False
        self.file = path_to_file
        self.play_sound = False

    def play(self):
        self.play_sound = True

    def run(self):
        self.running = True
        while self.running:

            if self.play_sound is True:
                playsound(self.file)
                self.play_sound = False
            else:
                time.sleep(0.05)