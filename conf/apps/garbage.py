import appdaemon.plugins.hass.hassapi as hass
import jdatetime
import datetime


class Garbage(hass.Hass):
    def initialize(self):
        self.garbage_done = False
        time = datetime.time(5, 0, 0)
        self.run_daily(self.set_garbage_done, time, status=False)
        self.run_hourly(self.check_garbage_day, time)

    def set_garbage_done(self, kwargs={}):
        light = self.get_app("lights")
        status = kwargs.get("status", True)
        self.log("setting the garbage done: " + str(status))
        self.garbage_done = status
        if status:
            light.neolight_color(0, 0, 0)

    def is_garbage_day(self):
        day = jdatetime.date.today().day
        return day % 2 == 0

    def check_garbage_day(self, kwargs):
        self.log('Checking garbage day')
        if self.is_garbage_day():
            self.set_state('binary_sensor.garbage_day', state="YES")
            is_set = self.get_state('input_boolean.garbage_day') == 'on'
            now_time = datetime.datetime.now().time()
            is_time = now_time > datetime.time(
                hour=21) and now_time < datetime.time(hour=23)
            if is_set and is_time:
                self.turn_on_light()
                self.announce()
        else:
            self.set_state('binary_sensor.garbage_day', state="NO")

    def turn_on_light(self):
        light = self.get_app("lights")
        self.log("Turning on neolight")
        light.neolight_notification(255, 63, 0)

    def announce(self):
        sound = self.get_app("sound")
        self.log('Announcing garbage day')
        sound.say('Garbage day!')
