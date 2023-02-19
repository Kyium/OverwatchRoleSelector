
from json import load, JSONDecodeError, dumps


PATH_TO_CONFIG = "../config.json"


class Config:
    def __init__(self, path_to_json_config: str, defaults: dict, create_on_load_fail: bool = True):
        self.path = path_to_json_config
        self.default_config = defaults
        self.creation = create_on_load_fail
        self.load_failed = False

        self.configs = {}
        self.__load_file()

    def __load_file(self):
        try:
            self.configs = load(open(self.path, encoding="UTF-8"))
        except JSONDecodeError:
            self.load_failed = True
            self.configs = self.default_config
            if self.creation:
                self.__write_data()

    def get(self, key: str):
        try:
            return self.configs[key]
        except KeyError:
            raise KeyError(f"Unknown config option '{key}'")

    def set(self, key: str, value):
        try:
            self.configs[key] = value
            if not self.load_failed:
                self.__write_data()
        except KeyError:
            raise KeyError(f"Unknown config option '{key}'")

    def get_all(self) -> dict:
        return self.configs.copy()

    def __write_data(self):
        config_data = dumps(self.configs)
        with open(self.path, "w") as f:
            f.write(config_data)


if __name__ == '__main__':
    test = Config(path_to_json_config=PATH_TO_CONFIG, defaults={'Test': 123})
    test.get("Test")
