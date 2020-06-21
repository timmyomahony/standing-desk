import redis

import dothat.touch as touch

from standing_desk.settings import REDIS_CHANNEL


class Buttons:
    redis_server = None
    redis_pubsub = None
    redis_channel = None
    update_thread = None

    def __init__(self, desk):
        self.desk = desk

        # Subscribe to redis
        self.redis_server = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_pubsub = self.redis_server.pubsub()
        self.redis_pubsub.psubscribe(REDIS_CHANNEL)

        # Up
        touch._cap1166.on(
            channel=touch.UP,
            event='press',
            handler=self.on_up_pressed())
        touch._cap1166.on(
            channel=touch.UP,
            event='release',
            handler=self.on_up_released())
        # Right = Up Preset
        touch._cap1166.on(
            channel=touch.RIGHT,
            event='press',
            handler=self.on_up_preset_pressed())
        # Left = Down Preset
        touch._cap1166.on(
            channel=touch.LEFT,
            event='press',
            handler=self.on_down_preset_pressed())
        # Down
        touch._cap1166.on(
            channel=touch.DOWN,
            event='press',
            handler=self.on_down_pressed())
        touch._cap1166.on(
            channel=touch.DOWN,
            event='release',
            handler=self.on_down_released())
        # Button
        touch._cap1166.on(
            channel=touch.BUTTON,
            event='press',
            handler=self.on_button_pressed())

    def __del__(self):
        self.redis_pubsub.unsubscribe()

    def on_up_pressed(self):
        def func(ch, event):
            self.redis_server.publish(REDIS_CHANNEL, 'up_start')
        return func

    def on_up_released(self):
        def func(ch, event):
            self.redis_server.publish(REDIS_CHANNEL, 'up_stop')
        return func

    def on_down_pressed(self):
        def func(ch, event):
            self.redis_server.publish(REDIS_CHANNEL, 'down_start')
        return func

    def on_down_released(self):
        def func(ch, event):
            self.redis_server.publish(REDIS_CHANNEL, 'down_stop')
        return func

    def on_button_pressed(self):
        def func(ch, event):
            self.redis_server.publish(REDIS_CHANNEL, 'toggle')
        return func

    def on_up_preset_pressed(self):
        def func(ch, event):
            self.redis_server.publish(REDIS_CHANNEL, 'up_preset')
        return func

    def on_down_preset_pressed(self):
        def func(ch, event):
            self.redis_server.publish(REDIS_CHANNEL, 'down_preset')
        return func
