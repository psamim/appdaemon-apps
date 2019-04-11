import appdaemon.plugins.hass.hassapi as hass
import datetime
import os

from androidtv import AndroidTV


class AndroidTv(hass.Hass):

    def initialize(self):
        self.android = AndroidTV(
            '192.168.31.137:5555', adbkey='{}/.android/adbkey'.format(os.path.expanduser('~')))
        # self.listen_state(self.get_attributes, "media_player.android_tv")
        self.log("android tv available: {}".format(self.android.available))

    def open_app(self, package):
        self.log("open app"+package)
        self.android._adb_shell_python_adb("monkey -p {} 1".format(package))

    def get_app_id(self):
        self.adroidtv_attributes = self.get_state(
            "media_player.android_tv", attribute="attributes")
        self.app_id = self.adroidtv_attributes.get("app_id")
        return self.app_id

    def is_available(self):
        return self.android.available
