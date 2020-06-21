import threading
import time

import dothat.backlight as backlight

from standing_desk.settings import MAX_HEIGHT, MIN_HEIGHT


class Lightbar(threading.Thread):

    def __init__(self, desk):
        self.desk = desk
        threading.Thread.__init__(self)
        self.update()

    def run(self):
        while True:
            # Only update when moving
            if self.desk.direction is not None:
                self.update()
            time.sleep(.1)

    def update(self):
        x = (self.desk.height - MIN_HEIGHT)/(MAX_HEIGHT - MIN_HEIGHT)
        x = round(x, 1)
        if x < .1:
            x = .1
        backlight.set_graph(x)
