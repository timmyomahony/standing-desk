import threading
import time

from standing_desk.distance import get_distance as get_height


class Desk(threading.Thread):
    height = None
    direction = None

    relay = None
    lightbar = None
    buttons = None
    display = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.height = get_height()

    def run(self):
        while True:
            # Only update when moving
            if self.direction is not None:
                accurate = False
                # 2 readings need to be within a cm of each other
                while not accurate:
                    h1 = get_height()
                    h2 = get_height()
                    accurate = abs(h1 - h2) < 2
                self.height = h1
            time.sleep(.1)
