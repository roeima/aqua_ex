from typing import Dict, Optional
import logging

import six
import yaml
from yaml import YAMLError
import copy


FORMAT = '%(asctime)s -- %(levelname)s -- %(message)s '
logging.basicConfig(format=FORMAT)
logger: logging.Logger = logging.getLogger(__name__)


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
        if not self.yml_dict:
            try:
                self.__load_dict()
            except Exception as e:
                logger.error(f'Error while loading yaml file (file_path={self.file_path}) -- {e}')
                return

        try:
            self.yml_dict = self.__merge(copy.deepcopy(self.yml_dict), extra_config)
        except Exception as e:
            logger.error(f'Error while merging, {e}')

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

    def save(self, filename=None):
        if not filename:
            filename = self.file_path
        with open(filename, 'w') as fp:
            yaml.dump(self.yml_dict, fp)

