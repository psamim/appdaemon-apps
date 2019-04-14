import appdaemon.plugins.hass.hassapi as hass
import datetime
import os

from androidtv import AndroidTV


class AndroidTVApp(hass.Hass):

    def initialize(self):
        self.android = AndroidTV(
            '192.168.31.137:5555', adbkey='{}/.android/adbkey'.format(os.path.expanduser('~')))
        # self.listen_state(self.get_attributes, "media_player.android_tv")
        self.log("android tv available: {}".format(self.android.available))

    def get_android(self):
        if not self.android.available:
            self.android = AndroidTV(
                '192.168.31.137:5555', adbkey='{}/.android/adbkey'.format(os.path.expanduser('~')))

        return self.android

    def open_app(self, package):
        android = self.get_android()
        self.log("open app: "+package)
        android._adb_shell_python_adb("monkey -p {} 1".format(package))

    def get_current_app_id(self):
        self.adroidtv_attributes = self.get_state(
            "media_player.android_tv", attribute="attributes")
        current_app_id = self.adroidtv_attributes.get("app_id")
        return current_app_id

    def is_available(self):
        android = self.get_android()
        return android.available
