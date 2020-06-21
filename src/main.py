import RPi.GPIO as GPIO 
import atexit

from standing_desk.relay import Relay
from standing_desk.display import Display
from standing_desk.buttons import Buttons
from standing_desk.lightbar import Lightbar
from standing_desk.desk import Desk


if __name__ == "__main__":
    desk = Desk()
    buttons = Buttons(desk)
    relay = Relay(desk)
    display = Display(desk)
    lightbar = Lightbar(desk)

    desk.buttons = buttons
    desk.relay = relay
    desk.display = display
    desk.lightbar = lightbar

    desk.start()
    lightbar.start()
    display.start()

    def exit_handler():
        print("Exiting ...")
        del relay
        del display
        del lightbar
        del buttons
        del desk

        GPIO.cleanup()

    atexit.register(exit_handler)
