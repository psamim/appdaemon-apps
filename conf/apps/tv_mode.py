import appdaemon.plugins.hass.hassapi as hass
import datetime


class TvMode(hass.Hass):
    tv_mode_last_played = "none"
    previous_type = "idle"

    def initialize(self):
        self.listen_state(self.on_kodi_change, "media_player.kodi")

    def on_kodi_change(self, entity, attribute, old, new, kwargs):
        mode = self.get_app("mode")
        sound = self.get_app("sound")
        lights = self.get_app("lights")
        kodi = self.get_app("kodi")

        current_mode = mode.get_mode()
        media_title = kodi.get_media_title()
        media_series_title = kodi.get_media_series_title()
        media_episode = str(kodi.get_media_episode())
        media_content_type = kodi.get_media_content_type()

        if media_content_type != self.previous_type and media_content_type != None:
            self.previous_type = media_content_type

        if current_mode == "TV":

            if media_content_type == "tvshow" or media_content_type == "movie":
                if self.tv_mode_last_played != media_content_type and new == 'playing':
                    self.tv_mode_last_played = media_content_type
                    lights.turn_off_all_lights()
                    if media_content_type == "tvshow" and self.now_is_between("sunset", "sunrise"):
                        lights.light("doorway", "on")

                elif old == 'paused' and new == 'playing' and self.now_is_between("sunset", "sunrise"):
                    lights.light("under_cabinet", "off")
                elif old == 'playing' and new == 'paused' and self.now_is_between("sunset", "sunrise"):
                    lights.light("under_cabinet", "on")

                if new == "playing" and old == 'idle':
                    if media_content_type == "movie":
                        sound.say('playing {}. Enjoy!'.format(media_title))
                    if media_content_type == "tvshow":
                        sound.say('playing {}, episode {}.{}. Enjoy!'.format(
                            media_series_title, media_episode, media_title))

            if old == 'playing' and new != "playing" and self.previous_type == 'music':
                lights.neolight_color(0, 0, 0)
            if old == 'playing' and new == "idle" and self.previous_type != 'music' and self.now_is_between("sunset", "sunrise"):
                lights.light("under_cabinet", "on")
            if new == 'playing' and media_content_type == "music":
                lights.neolight_effect("jackcandle")
