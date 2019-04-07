import appdaemon.plugins.hass.hassapi as hass
import datetime


class ModeNavigate(hass.Hass):

    def initialize(self):
        time = datetime.time(5, 0, 0)
        self.run_daily(self.go_to_normal, time)

    def go_to_normal(self):
        self.call_service(
            'scene/turn_on',
            entity_id="scene.normal"
        )
