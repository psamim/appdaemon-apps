import appdaemon.plugins.hass.hassapi as hass

class Dialogflow(hass.Hass):

    def initialize(self):
        self.register_endpoint(self.api_call, "dialogflow")

    def api_call(self, data):
        self.log(data)
        return '{ "fulfillmentText": "This is hass talking" }' , 200

