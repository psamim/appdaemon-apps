import appdaemon.plugins.hass.hassapi as hass

GARBAGE_INTENT_NAME = "projects/newagent-bd916/agent/intents/6c5624a3-837b-49cf-90a1-6f537464ea71"
GARBAGE_DONE_INTENT_NAME = "projects/newagent-bd916/agent/intents/e6ed62be-fb38-419b-8268-ba4fb6a80d2f"
PLAY_MOVIE = "projects/newagent-bd916/agent/intents/e48fcd42-3374-4430-a303-4189ecc34332"


class Dialogflow(hass.Hass):
    def initialize(self):
        self.register_endpoint(self.api_call, "dialogflow")

    def api_call(self, data):
        self.log(data)

        query_result = data.get("queryResult")
        name = None
        intent = None

        if query_result is not None:
            intent = query_result.get("intent")
        if intent is not None:
            name = intent.get("name")

        self.log("Q: " + str(query_result))
        self.log("I: " + str(intent))
        self.log("N: " + str(name))

        if name == GARBAGE_INTENT_NAME:
            self.log("Garbage intent recieved")
            garbage = self.get_app("garbage")
            if garbage.is_garbage_day():
                return '{ "fulfillmentText": "Yes" }', 200
            else:
                return '{ "fulfillmentText": "no" }', 200

        if name == GARBAGE_DONE_INTENT_NAME:
            garbage = self.get_app("garbage")
            garbage.set_garbage_done()
            return '{ "fulfillmentText": "OK" }', 200

        if name == PLAY_MOVIE:
            parameters = query_result.get("parameters")
            if parameters is not None:
                movie = parameters.get("movie")
                kodi = self.get_app("kodi")
                found = kodi.find_movie(movie)
                self.log(found)
                if len(found):
                    return '{ "fulfillmentText": "{}" }'.format(
                        found[0].get("label")), 200
                else:
                    return '{ "fulfillmentText": "Not found" }', 200

        return '{ "fulfillmentText": "This is hass talking" }', 200
