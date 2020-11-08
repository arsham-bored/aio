import json

class Config:

    def __init__(self):
        self.body = self.load()

    class ConfigNotExistsError(Exception):
        pass

    @classmethod
    def load(self):
        try:
            with open("config.json") as config_file:
                return json.load(config_file)

        except FileNotFoundError as error:
            raise self.ConfigNotExistsError(error)

    @property
    def token(self):
        return self.body['token']

    @property
    def boost_time(self):
        return self.body['time']['boost']

    @property
    def limit_time(self):
        return self.body['time']['limit_time']

    @property
    def name(self):
        return self.body['name']