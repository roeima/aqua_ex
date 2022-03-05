import yaml


class YamlEditor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = self.__load_file()
        self.file_dict = None

    def __load_file(self):
        return open(self.file_path, 'r+')

    def __load_dict(self):
        return yaml.safe_load(self.file)

    def add_config(self, config_key, value):
        pass

    def save(self):
        if not self.file_dict:
            self.__load_dict()
        yaml.dump(self.file_dict, self.file)

    def close(self):
        self.file.close()
