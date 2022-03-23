import unittest
from unittest import mock

from src.yml_editor import YamlEditor, YamlEditorException


class YamlEditorTest(unittest.TestCase):

    def setUp(self) -> None:
        yml_for_test = {
            'roei': 1,
            'roei_dictionary': {
                'x': {
                    'y': 1
                }
            }
        }
        self.editor = YamlEditor('')
        self.safe_load_pathcer = mock.patch('src.yml_editor.yaml.safe_load', return_value=yml_for_test)
        self.file_load_pathcer = mock.patch.object(YamlEditor, '_YamlEditor__load_file', return_value=None)
        self.file_load_pathcer.start()
        self.safe_load_pathcer.start()

    def test_add_config(self):
        # add new value to yml
        self.editor.add_config({'roei2': 1})
        self.assertEqual(self.editor.yml_dict['roei2'], 1)

        # add value to a single value field
        self.editor.add_config({'roei2': 1})
        self.assertEqual(self.editor.yml_dict['roei2'], [1, 1])

        # add single value to list
        self.editor.add_config({'roei2': 1})
        self.assertEqual(self.editor.yml_dict['roei2'], [1, 1, 1])

        # add list to list
        self.editor.add_config({'roei2': [1, 1]})
        self.assertEqual(self.editor.yml_dict['roei2'], [1, 1, 1, 1, 1])

        # add a null value to yml
        self.editor.add_config({'roei_null': None})
        self.assertEqual(self.editor.yml_dict['roei_null'], None)

        # test exception when adding a list or a single value to a taken key
        self.assertRaises(YamlEditorException, self.editor.add_config, {'roei_dictionary': [1, 2, 3]})
        self.assertRaises(YamlEditorException, self.editor.add_config, {'roei_dictionary': 1})

        # test primitive type only
        class Person:
            def __init__(self):
                pass
        p = Person()
        self.assertRaises(YamlEditorException, self.editor.add_config, {'person': p})

    def tearDown(self) -> None:
        self.safe_load_pathcer.stop()
        self.file_load_pathcer.stop()


if __name__ == '__main__':
    unittest.main()