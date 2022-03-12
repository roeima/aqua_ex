from typing import Dict, Optional
import logging

import six
import yaml
from yaml import YAMLError
import copy


FORMAT = '%(asctime)s -- %(levelname)s -- %(message)s '
logging.basicConfig(format=FORMAT)
logger: logging.Logger = logging.getLogger(__name__)


def nested_dict_values(d):
    for v in d.values():
        if isinstance(v, dict):
            yield from nested_dict_values(v)
        else:
            yield v


class YamlEditorException(Exception):
    pass


class YamlEditor:

    def __init__(self, file_path):
        self.file_path = file_path
        self.yml_dict: Optional[Dict] = None

    def __load_file(self):
        try:
            return open(self.file_path, 'r+')
        except FileNotFoundError as e:
            logger.error(f'{self.file_path} File Not Found')
            raise e

    def __load_dict(self):
        try:
            file = self.__load_file()
            self.yml_dict = yaml.safe_load(file)
        except FileNotFoundError as e:
            raise e
        except YAMLError as e:
            logger.error(f'Yaml Error - {e}')
            raise e

    def add_config(self, extra_config: Dict):
        if not self.check_extra_config(extra_config):
            raise YamlEditorException('extra config are not using yaml datatypes')
        if not self.yml_dict:
            try:
                self.__load_dict()
            except Exception as e:
                logger.error(f'Error while loading yaml file (file_path={self.file_path}) -- {e}')
                raise e

        try:
            self.yml_dict = self.__merge(copy.deepcopy(self.yml_dict), extra_config)
        except Exception as e:
            logger.error(f'Error while merging, {e}')
            raise e

    def __merge(self, base_dict, added_dict):
        try:
            if base_dict is None or isinstance(base_dict, (six.string_types, float, six.integer_types)):
                value = list()
                value.append(base_dict)
                if isinstance(added_dict, list):
                    value.extend(added_dict)
                else:
                    value.append(added_dict)

                base_dict = value

            elif isinstance(base_dict, list):

                if isinstance(added_dict, list):
                    base_dict.extend(added_dict)
                else:
                    base_dict.append(added_dict)

            elif isinstance(base_dict, dict):

                if isinstance(added_dict, dict):
                    for key in added_dict:
                        if key in base_dict:
                            base_dict[key] = self.__merge(base_dict[key], added_dict[key])
                        else:
                            base_dict[key] = added_dict[key]
                else:
                    raise YamlEditorException(f'Cannot merge non-dict {added_dict} into dict {base_dict}')
            else:
                raise YamlEditorException(f'Not implemented {added_dict} into {base_dict}')
        except Exception as e:
            raise e

        return base_dict

    @staticmethod
    def check_extra_config(extra_config):
        # checks for not primitive type in extra config
        for v in nested_dict_values(extra_config):
            if not (v is None or isinstance(v, (six.string_types, float, six.integer_types, list))):
                return False
        return True

    def save(self, filename=None):
        if self.yml_dict is None:
            return
        if not filename:
            filename = self.file_path
        with open(filename, 'w') as fp:
            yaml.dump(self.yml_dict, fp)

