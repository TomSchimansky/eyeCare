import time


class Timer(object):
    def __init__(self, fps, printing=False):
        self.fps = fps
        self.time_1 = 0
        self.time_2 = time.time()
        self.printing = printing

    def wait(self):
        self.time_1 = time.time()

        spend_time = self.time_1 - self.time_2
        sleep_time = 1/self.fps - spend_time

        if sleep_time < 0:
            if self.printing:
                print("[Timer] Delay of", str(round(-sleep_time, 4)), "secs")
        else:
            time.sleep(sleep_time)

        self.time_2 = time.time()


class StopWatch:
    def __init__(self):
        self.time_elapsed = 0
        self.start_time = 0
        self.running = False

    def get_elapsed(self):
        if self.running is True:
            return self.time_elapsed + (time.time() - self.start_time)
        else:
            return self.time_elapsed

    def is_running(self):
        return self.running

    def start(self):
        if self.running is False:
            self.running = True
            self.start_time = time.time()

    def stop(self):
        if self.running is True:
            self.running = False
            self.time_elapsed += time.time() - self.start_time

    def reset(self):
        self.running = False
        self.time_elapsed = 0
        self.start_time = 0
