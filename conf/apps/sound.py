import appdaemon.plugins.hass.hassapi as hass


class Sound(hass.Hass):

    def initialize(self):
        pass

    def say(self, messege):
        self.log("tts: {}".format(messege))
        self.call_service(
            'tts/google_say',
            entity_id='media_player.google_home',
            message=messege)
