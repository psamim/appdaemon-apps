import appdaemon.plugins.hass.hassapi as hass
import datetime


class Mode(hass.Hass):
    tv_mode_last_played = "none"
    previous_type = "idle"

    def initialize(self):
        time = datetime.time(5, 0, 0)
        self.run_daily(self.set_mode('normal'), time)
        self.listen_state(self.on_mode_change, "input_select.mode")

    def set_mode(self, mode):
        self.call_service(
            'input_select/select_option',
            entity_id="input_select.mode",
            option=mode
        )

    def get_mode(self):
        return self.get_state('input_select.mode')

    def on_mode_change(self, entity, attribute, old, new, kwargs):
        if new == old:
            return
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
            # sound.say('Normal mode')
            kodi.notify(
                "Normal Mode", "Mode Changed", "smb://192.168.31.20/share/Kodi/icons/hologram.png")
        elif new == "Not home":
            self.log("Not home mode entered")
