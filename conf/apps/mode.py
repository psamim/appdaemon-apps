import appdaemon.plugins.hass.hassapi as hass
import datetime

INPUT_MODE = "input_select.mode"


class Mode(hass.Hass):
    tv_mode_last_played = "none"
    previous_type = "idle"

    def initialize(self):
        time = datetime.time(5, 0, 0)
        self.listen_state(self.on_kodi_change, "media_player.kodi")
        self.listen_state(self.on_mode_change, INPUT_MODE)

    def on_mode_change(self, entity, attribute, old, new, kwargs):
        kodi = self.get_app("kodi")
        sound = self.get_app("sound")
        if new == "TV":
            self.log("TV mode entered")
            sound.say('TV mode activated!')
            kodi.notify(
                "TV Mode Activated", "Mode Changed", "smb://192.168.31.20/share/Kodi/icons/movie.png")
            self.tv_mode_last_played = 'none'
        elif new == "Normal":
            self.log("Normal mode entered")
            sound.say('Normal mode')
            kodi.notify(
                "Normal Mode", "Mode Changed", "smb://192.168.31.20/share/Kodi/icons/hologram.png")

    def on_kodi_change(self, entity, attribute, old, new, kwargs):
        lights = self.get_app("lights")
        mode = self.get_state(INPUT_MODE)
        kodi_attributes = self.get_state(
            "media_player.kodi", attribute="attributes")

        self.log("previous_type: " + str(self.previous_type))
        type = kodi_attributes.get("media_content_type")
        if type != self.previous_type:
            self.previous_type = type
        media_title = kodi_attributes.get("media_title")
        media_title = kodi_attributes.get("media_title")
        media_series_title = kodi_attributes.get("media_series_title")
        media_episode = str(kodi_attributes.get("media_episode"))

        self.log("new on change: " + new)
        self.log("old on change: " + old)

        self.log("kodi_attributes: " + str(kodi_attributes))
        self.log("Mode: " + mode)
        self.log("type: " + str(type))
        self.log("media_title: " + (media_title or "none"))
        self.log("media_series_title: " + (media_series_title or "none"))
        self.log("media_episode: " + (media_episode or 0))

        if mode == "TV":
            self.tv_mode(new, type, lights, media_title,
                         media_series_title, media_episode, old)

    def tv_mode(self, new, type, lights, media_title, media_series_title, media_episode, old):
        sound = self.get_app("sound")
        if type == "tvshow" or type == "movie":
            if self.tv_mode_last_played != type and new == 'playing':
                self.tv_mode_last_played = type
                lights.turn_off_all_lights()
                if type == "tvshow":
                    lights.light("doorway", "on")

            elif old == 'paused' and new == 'playing':
                lights.light("under_cabinet", "off")
            elif old == 'playing' and new == "paused":
                lights.light("under_cabinet", "on")

            if new == "playing" and old == 'idle':
                if type == "movie":
                    sound.say('playing {}. Enjoy!'.format(media_title))
                if type == "tvshow":
                    sound.say('playing {}, episode {}.{}. Enjoy!'.format(
                        media_series_title, media_episode, media_title))

        if old == 'playing' and new != "playing" and self.previous_type == "music":
            self.log("stop music")
            lights.neolight_color(0, 0, 0, 0)
        if old == 'playing' and new == "idle" and self.previous_type != "music":
            lights.light("under_cabinet", "on")
        if new == 'playing' and type == "music":
            self.log("JACK")
            lights.neolight_effect("jackcandle")

    def tv_mode_first_time(self, lights, type, media_title, media_series_title, media_episode):
        self.log("first time after TV mode entered")

        self.tv_mode_last_played = type
        lights.turn_off_all_lights()

        if type == "tvshow":
            lights.light("doorway", "on")
