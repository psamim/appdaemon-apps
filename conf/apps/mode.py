import appdaemon.plugins.hass.hassapi as hass
import datetime

INPUT_MODE = "input_select.mode"


class Mode(hass.Hass):
    is_tv_mode_first_played = False

    def initialize(self):
        time = datetime.time(0, 0, 0)
        self.listen_state(self.on_kodi_change, "media_player.kodi")
        self.listen_state(self.on_mode_change, INPUT_MODE)

    def publish_kodi_notification(self, title, message, image):
        self.call_service(
            'media_player/kodi_call_method',
            entity_id="media_player.kodi",
            method="GUI.ShowNotification",
            title=title,
            message=message,
            image=image,
            displaytime=3000
        )

    def on_mode_change(self, entity, attribute, old, new, kwargs):
        if new == "TV" and old == "Normal":
            self.log("TV mode entered")
            self.publish_kodi_notification(
                "TV Mode Activated", "Mode Changed", "smb://192.168.31.20/share/Kodi/icons/movie.png")
            self.is_tv_mode_first_played = True
        elif new == "Normal":
            self.log("Normal mode entered")
            self.publish_kodi_notification(
                "Normal Mode Activated", "Mode Changed", "smb://192.168.31.20/share/Kodi/icons/hologram.png")

    def on_kodi_change(self, entity, attribute, old, new, kwargs):
        mode = self.get_state(INPUT_MODE)
        kodi_attributes = self.get_state(
            "media_player.kodi", attribute="attributes")
        type = kodi_attributes.get("media_content_type")

        self.log("new on change: " + new)
        self.log("kodi_attributes: " + str(kodi_attributes))
        self.log("Mode: " + mode)
        self.log("type: " + (type or "none"))

        if mode == "TV":
            if self.is_tv_mode_first_played == True and new == 'playing' and (type == "tvshow" or type == "movie"):
                self.log("im here 0")
                self.is_tv_mode_first_played = False
            elif new == 'playing' and (type == "tvshow" or type == "movie"):
                self.log("im here 1")
            elif old == 'playing' and new == "paused" and (type == "tvshow" or type == "movie"):
                self.log("im here 2")
            elif new == 'playing' and type == "song":
                self.log("im here 3")

    def run(self, kwargs):
        self.log("hello")
        self.call_service(
            'media_player/kodi_call_method',
            entity_id="media_player.kodi",
            method="JSONRPC.Permission"
        )
