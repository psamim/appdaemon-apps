import appdaemon.plugins.hass.hassapi as hass


class Lights(hass.Hass):
    def initialize(self):
        pass

    def turn_off_all_lights(self):
        self.call_service(
            'light/turn_off',
            entity_id='group.all_lights')

    def light(self, light_name, status):
        self.call_service(
            'light/turn_{}'.format(status),
            entity_id='light.{}'.format(light_name))

    def neolight_color(self, r, g, b, w):
        self.call_service(
            'mqtt/publish',
            payload="{},{},{}".format(r, g, b),
            topic="/home/neolight/neolight/color/set")
        self.call_service(
            'mqtt/publish',
            payload="{}".format(w),
            topic="/home/neolight/neolight/brightness/set")

    def neolight_effect(self, effect):
        self.call_service(
            'mqtt/publish',
            payload=effect,
            topic="/home/neolight/neolight/effect/set")

    def neolight_notification(self, r, g, b, s1="025", s2=3000):
        self.call_service(
            'mqtt/publish',
            payload="{},{},{},{},{}".format(r, g, b, s1, s2),
            topic="/home/neolight/neolight/notification/set")
