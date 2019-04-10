import appdaemon.plugins.hass.hassapi as hass

GARBAGE_INTENT_NAME = "projects/newagent-bd916/agent/intents/6c5624a3-837b-49cf-90a1-6f537464ea71"

class Dialogflow(hass.Hass):

    def initialize(self):
        self.register_endpoint(self.api_call, "dialogflow")

    def api_call(self, data):
        self.log(data)
        self.log("type" + str(type(data)))
       

        intent = data.get("intent")
        self.log("intent" + str(intent))
        name = ""
        if intent is not None:
            name = intent.get("name")

        if name is GARBAGE_INTENT_NAME:
            garbage = self.get_app("garbage")
            if garbage.is_garbage_day():
                return '{ "fulfillmentText": "Yes, it is" }' , 200
            return '{ "fulfillmentText": "no, it\'s not" }' , 200
            
        return '{ "fulfillmentText": "This is hass talking" }' , 200

