import time


class FadeAlpha:
    def __init__(self, from_, to, duration=1000):
        self.from_ = from_
        self.general_delta = to - from_
        self.duration = duration
        self.left, self.right = min(from_, to), max(from_, to)
        self.reset()

    def reset(self):
        self.current_value = self.from_
        self.last_time = None

    def __call__(self, color):
        now = time.time()
        if self.last_time is not None:
            time_delta = self.duration / ((now - self.last_time) * 1000)
            self.current_value += (self.general_delta / time_delta)
            if self.current_value <= self.left:
                self.current_value = self.right
            if self.current_value > self.right:
                self.current_value = self.left
        color.a = round(self.current_value)
        self.last_time = now