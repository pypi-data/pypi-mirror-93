import json


class Config:
    def __init__(self):
        self.json_encoder = json.JSONEncoder

    def set_json_encoder(self, encoder):
        self.json_encoder = encoder


config = Config()
