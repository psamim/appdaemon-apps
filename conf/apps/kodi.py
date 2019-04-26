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
        androidtv = self.get_app("androidtv")
        androidtv.turn_on()
        androidtv.open_app("org.xbmc.kodi")
        response = request(URL, "VideoLibrary.GetMovies")
        movies = response.data.result.get("movies", None)

        def remove_extra_chars1(movie):
            label = re.sub("[-:]", "", movie.get("label"))
            return {**movie, "label": label}

        def remove_extra_chars2(movie):
            label = re.sub("-", " ", movie.get("label"))
            return {**movie, "label": label}

        if movies is None:
            return

        edited_movies1 = list(
            map(remove_extra_chars1, movies))
        edited_movies2 = list(
            map(remove_extra_chars2, movies))
        edited_movies = edited_movies1 + edited_movies2 + movies

        found = list(
            filter(lambda m: re.search(pattern, m.get("label"), re.IGNORECASE),
                   edited_movies))
        sorted_movies = list(sorted(found, key=lambda s: len(
            s.get("label"))))
        return sorted_movies

    def play_movie(self, movie_id):
        request(URL, "Player.Open", item={"movieid": movie_id})

    def find_artist(self, pattern):
        androidtv = self.get_app("androidtv")
        androidtv.turn_on()
        androidtv.open_app("org.xbmc.kodi")
        response = request(URL, "AudioLibrary.GetArtists")
        artists = response.data.result.get("artists", None)
        if artists is None:
            return

        found = list(
            filter(lambda m: re.search("\\b"+pattern+"s?\\b", m.get("label"), re.IGNORECASE),
                   artists))
        return found

    def play_song(self, artist_id):
        request(URL, "Player.Open", item={
                "artistid": artist_id}, options={"shuffled": True})
        request(URL, "GUI.SetFullscreen", fullscreen=True)

    def play_partymode(self):
        request(URL, "Player.Open", item={"partymode": "music"})

    def scan_library(self):
        request(URL, "VideoLibrary.Scan")

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
