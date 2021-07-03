import json
from typing import Set


class Configurator:

    def __init__(self, file_path: str, required_fields: Set = None):
        self.REQUIRED_KEYS = required_fields if required_fields is not None else {}
        with open(file_path) as json_config_file:
            self.config = json.load(json_config_file)
        self.__validate()

    def __validate(self):
        for key in self.REQUIRED_KEYS:
            if key not in self.config:
                raise ValueError('Missing parameter %s'.format(key))

    def get(self, key: str):
        configuration = self.config
        for single_key in key.split('.'):
            configuration = configuration[single_key] if single_key in configuration else None
        return configuration
