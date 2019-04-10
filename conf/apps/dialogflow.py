import appdaemon.plugins.hass.hassapi as hass

class Dialogflow(hass.Hass):

    def initialize(self):
        self.register_endpoint(self.api_call, "dialogflow")

    def api_call(self, data):
        intent = self.get_apiai_intent(data)
        self.log(data)

        if intent is None:
            self.log("Apiai error encountered: Result is empty")
            return "", 201

        self.log(intent)
        return "", 200

