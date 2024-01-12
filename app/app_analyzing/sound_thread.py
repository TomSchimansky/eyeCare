from threading import Thread
import pyaudio
import numpy as np
import time

from settings import Settings


class SoundThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)

        self.running = False
        self.volume = 0
        self.last_volume = 0

        self.chunk_size = 2048

        self.py_audio_object = pyaudio.PyAudio()
        self.audio_stream = self.py_audio_object.open(format=pyaudio.paFloat32,
                                                      channels=1,
                                                      rate=Settings.SAMPLE_RATE,
                                                      output=True,
                                                      stream_callback=self.audio_callback,
                                                      frames_per_buffer=self.chunk_size)

        self.sample_rate = Settings.SAMPLE_RATE
        self.last_x = 0
        self.time_array = np.linspace(0, self.chunk_size, self.chunk_size)

    def set_volume(self, volume):
        self.volume = volume

    def stop(self):
        self.running = False

    @staticmethod
    def linear_volume_fade(sample_data, last_volume, volume):
        return (sample_data * np.linspace(last_volume, volume, len(sample_data))).astype(np.float32)

    def audio_callback(self, in_data, frame_count, time_info, status):
        data = np.sin(2*np.pi*(self.time_array+self.last_x)*(261.626 / self.sample_rate)).astype(np.float32)  # C
        data += np.cos(2 * np.pi * (self.time_array + self.last_x) * (329.628 / self.sample_rate)).astype(np.float32)  # E
        data = data / 2

        self.last_x += self.chunk_size

        if self.last_volume != self.volume:
            data = self.linear_volume_fade(data, self.last_volume, self.volume)
        else:
            data = data * self.volume

        self.last_volume = self.volume

        return data, pyaudio.paContinue

    def run(self):
        self.running = True

        self.audio_stream.start_stream()

        while self.running:
            time.sleep(0.1)

        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.py_audio_object.terminate()


if __name__ == "__main__":
    # simple test

    s = SoundThread()
    s.start()

    s.set_volume(0.1)
    time.sleep(2)
    s.set_volume(0)

    s.set_volume(0.5)
    time.sleep(2)
    s.set_volume(0)

    s.stop()