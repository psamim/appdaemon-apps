import appdaemon.plugins.hass.hassapi as hass
import datetime


class Kodi(hass.Hass):

    def initialize(self):
        pass

    def notify(self, title, message, image=None):
        self.call_service(
            'media_player/kodi_call_method',
            entity_id="media_player.kodi",
            method="GUI.ShowNotification",
            title=title,
            message=message,
            image=image,
            displaytime=3000
        )
