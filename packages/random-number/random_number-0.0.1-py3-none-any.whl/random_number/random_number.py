from random import randint


class random_number:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def get_random_number(self):
        return randint(self.start, self.end)
