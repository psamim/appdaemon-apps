import appdaemon.plugins.hass.hassapi as hass


class Charge(hass.Hass):

    def initialize(self):
        self.listen_state(self.listen, 'device_tracker.192_168_31_217_e3_10_2b_34_55_2f')


    def listen(self, entity, attribute, old, new, kwargs):
        pass
