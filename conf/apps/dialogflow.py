import appdaemon.plugins.hass.hassapi as hass

class Dialogflow(hass.Hass):

    def initialize(self):
        pass

    def api_call(self, data):
        intent = self.get_apiai_intent(data)
        self.log(data)

        if intent is None:
            self.log("Apiai error encountered: Result is empty")
            return "", 201

        response = self.format_apaiai_response(speech = "I'm sorry, the {} does not exist within AppDaemon".format(intent))

        return response, 200

