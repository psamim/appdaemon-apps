import appdaemon.plugins.hass.hassapi as hass
from jsonrpcclient import request
import datetime
import re

URL = "http://192.168.31.137:8080/jsonrpc"


class Kodi(hass.Hass):
    def initialize(self):
        self.listen_state(self.get_attributes, "media_player.kodi")
        self.kodi_attributes = {}

    def find_movie(self, pattern):
        response = request(URL, "VideoLibrary.GetMovies")
        movies = response.data.result.get("movies", None)
        if movies is None:
            return

        found = list(
            filter(lambda m: re.search(pattern, m.get("label"), re.IGNORECASE),
                   movies))
        return found

    def notify(self, title, message, image=None):
        self.call_service('media_player/kodi_call_method',
                          entity_id="media_player.kodi",
                          method="GUI.ShowNotification",
                          title=title,
                          message=message,
                          image=image,
                          displaytime=3000)

    def get_attributes(self, entity, attribute, old, new, kwargs):
        self.kodi_attributes = self.get_state("media_player.kodi",
                                              attribute="attributes")
        return self.kodi_attributes

    def get_media_title(self):
        self.media_title = self.kodi_attributes.get("media_title")
        return self.media_title

    def get_media_series_title(self):
        self.media_series_title = self.kodi_attributes.get(
            "media_series_title")
        return self.media_series_title

    def get_media_episode(self):
        self.media_episode = self.kodi_attributes.get("media_episode")
        return self.media_episode

    def get_media_content_type(self):
        self.media_content_type = self.kodi_attributes.get(
            "media_content_type")
        return self.media_content_type
