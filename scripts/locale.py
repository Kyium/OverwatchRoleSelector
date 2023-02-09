class Locale:
    def __init__(self, locale_file_path: str):
        self.locale_file_path = locale_file_path
        self.lookup_dict = {}
        self.load_locale()

    def load_locale(self):
        try:
            with open(self.locale_file_path) as f:
                line = f.readline()
                while line:
                    try:
                        key, value = line.rstrip().split(",")
                    except ValueError:
                        pass
                    self.lookup_dict[key] = value
                    line = f.readline()
        except FileNotFoundError:
            pass

    def g(self, key: str) -> str:
        try:
            return self.lookup_dict[key]
        except KeyError:
            return "???"
