"""
Relay controller

A simple script that listends to redis for incoming commands and operates
the relay switch

Available redis commands:

"down_start"
"down_stop"
"up_start"
"up_stop"
"""
import time
import redis
import RPi.GPIO as GPIO 

from standing_desk.settings import REDIS_CHANNEL, DESK_UP, DESK_DOWN, TOP_PRESET, BOTTOM_PRESET

GPIO_DOWN = 21
GPIO_UP = 20

GPIO_START = 0
GPIO_STOP = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_DOWN, GPIO.OUT)
GPIO.setup(GPIO_UP, GPIO.OUT)


class Relay:
    redis_server = None
    redis_pubsub = None
    redis_thread = None

    def __init__(self, desk):
        self.desk = desk

        def redis_handler(msg):
            func = getattr(self, msg['data'])
            func()

        # Subscribe to redis
        self.redis_server = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_pubsub = self.redis_server.pubsub()
        self.redis_pubsub.psubscribe(**{
            '{0}*'.format(REDIS_CHANNEL): redis_handler
        })
        self.redis_thread = self.redis_pubsub.run_in_thread(sleep_time=0.001)

    def __del__(self):
        self.redis_pubsub.unsubscribe()
        self.redis_thread.stop()

    def down_start(self):
        self.desk.direction = DESK_DOWN
        GPIO.output(GPIO_UP, GPIO_STOP)
        GPIO.output(GPIO_DOWN, GPIO_START)

    def down_stop(self):
        self.desk.direction = None
        GPIO.output(GPIO_UP, GPIO_STOP)
        GPIO.output(GPIO_DOWN, GPIO_STOP)

    def up_start(self):
        self.desk.direction = DESK_UP
        GPIO.output(GPIO_DOWN, GPIO_STOP)
        GPIO.output(GPIO_UP, GPIO_START)

    def up_stop(self):
        self.desk.direction = None
        GPIO.output(GPIO_DOWN, GPIO_STOP)
        GPIO.output(GPIO_UP, GPIO_STOP)

    def up_preset(self):
        if self.desk.height < BOTTOM_PRESET + 5:  # 5 is a threshold
            self.up_start()
            while self.desk.height < TOP_PRESET:
                time.sleep(.1)
            self.up_stop()

    def down_preset(self):
        if self.desk.height > TOP_PRESET - 5:
            self.down_start()
            while self.desk.height > BOTTOM_PRESET:
                time.sleep(.1)
            self.down_stop()
