import yaml
import re


def flatten(dictionary, parent_key=False, separator='.'):
    items = []
    for key, value in dictionary.items():
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten(value, new_key, separator).items())
        elif isinstance(value, list):
            for k, v in enumerate(value):
                items.extend(flatten({str(k): v}, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)


def unflatten(flat_dict):
    sorted_flat_dict = dict(sorted(flat_dict.items()))
    result_dict = {}
    for key, value in sorted_flat_dict.items():
        s = result_dict
        tokens = re.findall(r'\w+', key)
        for count, (index, next_token) in enumerate(zip(tokens, tokens[1:] + [value]), 1):
            value = next_token if count == len(tokens) else [] if next_token.isdigit() else {}
            if isinstance(s, list):
                index = int(index)
                while index >= len(s):
                    s.append(value)
            elif index not in s:
                s[index] = value
            s = s[index]
    return result_dict


# TODO adding context manager
class YamlEditor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = self.__load_file()
        self.file_dict = None

    def __load_file(self):
        return open(self.file_path, 'r+')

    def __load_yml(self):
        self.file_dict = yaml.safe_load(self.file)

    def add_config(self, config_key, value):
        if not self.file_dict:
            self.__load_yml()
        yml_flat = flatten(self.file_dict)

        if self.is_key_exists(config_key, yml_flat.keys()):
            origin_value = self.get_origin_value(config_key)
            start_config_pos = 0

            if isinstance(origin_value, list):
                start_config_pos = len(origin_value)
            else:
                start_config_pos = 1
                del yml_flat[config_key]
                new_key = self.get_key(0, config_key)
                yml_flat[new_key] = origin_value

            if not isinstance(value, list):
                added_key = self.get_key(start_config_pos, config_key)
                yml_flat[added_key] = value
            else:
                for idx, val in enumerate(value, start_config_pos):
                    added_key = self.get_key(idx, config_key)
                    yml_flat[added_key] = val
        elif self.check_entries(config_key):
            yml_flat[config_key] = value
        else:
            # print(config_key, self.check_entries(config_key))
            raise Exception(f'File contains key for {config_key}')

        self.file_dict = unflatten(flat_dict=yml_flat)

    def get_origin_value(self, flat_key):
        x = self.file_dict
        tokens = flat_key.split('.')
        for token in tokens:
            if token.isdigit():
                x = x[int(token)]
            else:
                x = x[token]
        return x

    @staticmethod
    def is_key_exists(key, yml_keys):
        if key in yml_keys:
            return True
        for k in yml_keys:
            if key in k:
                return True
        return False

    @staticmethod
    def get_key(config_pos, flat_key):
        tokens = flat_key.split('.')
        tokens.append(str(config_pos))
        key = '.'.join(tokens)
        return key

    def check_entries(self, flat_key):
        tokens = flat_key.split('.')
        x = self.file_dict
        for token in tokens:
            if not x:
                break
            if not (isinstance(x, list) or isinstance(x, dict)):
                return False

            if token.isdigit():
                token = int(token)
                x = x[token]
            else:
                x = x.get(token)
        return True

    def save(self, filename=None):
        if not self.file_dict:
            self.__load_yml()
        if not filename:
            yaml.dump(self.file_dict, self.file)
        else:
            with open(filename, 'w') as fp:
                yaml.dump(self.file_dict, fp)

    def close(self):
        self.file.close()
