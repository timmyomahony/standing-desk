import math
import time
import threading

import dothat.backlight as backlight
import dothat.lcd as lcd


CLEAR_LINE = "       "


class Display(threading.Thread):
    def __init__(self, desk):
        threading.Thread.__init__(self)
        self.desk = desk

        # Reset the LCD
        lcd.clear()
        self.update_height()

    def run(self):
        while True:
            self.update_backlight()
            # Only update when moving
            if self.desk.direction is not None:
                self.update_height()
            time.sleep(.1)

    def update_backlight(self):
        backlight.rgb(0, 255, 0)

    def update_height(self):
        self.clear_line(linenum=0)
        lcd.set_cursor_position(0, 0)
        lcd.write("{0} cm".format(round(self.desk.height, 2)))

    def clear_line(self, linenum=0):
        lcd.set_cursor_position(0, linenum)
        lcd.write(CLEAR_LINE)
