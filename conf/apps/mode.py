import appdaemon.plugins.hass.hassapi as hass
import datetime

from androidtv import AndroidTV


class Mode(hass.Hass):
    tv_mode_last_played = "none"
    previous_type = "idle"

    def initialize(self):
        #time = datetime.time(5, 0, 0)
        self.listen_state(self.on_mode_change, "input_select.mode")
        self.android = AndroidTV(
            '192.168.31.137:5555', adbkey='/home/homeassistant/.android/adbkey')

    def set_mode(self, mode):
        self.call_service(
            'input_select/select_option',
            entity_id="input_select.mode",
            option=mode
        )

    def get_mode(self):
        return self.get_state('input_select.mode')

    def on_mode_change(self, entity, attribute, old, new, kwargs):
        kodi = self.get_app("kodi")
        sound = self.get_app("sound")

        if new == "TV":
            self.log("TV mode entered")
            self.android._adb_shell_python_adb("monkey -p org.xbmc.kodi 1")
            sound.say('TV mode activated!')
            kodi.notify(
                "TV Mode Activated", "Mode Changed", "smb://192.168.31.20/share/Kodi/icons/movie.png")
            self.tv_mode_last_played = 'none'
        elif new == "Normal":

            self.log("Normal mode entered")
            sound.say('Normal mode')
            kodi.notify(
                "Normal Mode", "Mode Changed", "smb://192.168.31.20/share/Kodi/icons/hologram.png")
        elif new == "Not home":
            self.log("Not home mode entered")
