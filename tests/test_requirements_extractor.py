import unittest
from unittest import mock

from src.requirements_extractor import get_dir_requirements, get_connected_files, extract_requirements


class RequirementsExtractorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.requirements = {
            'requirements.txt': {
                'pkgs': ['PyYAML==6.0', 'requirements-parser==0.5.0', 'six==1.16.0', 'types-setuptools==57.4.10'],
                'files': ['requirements2.txt']
            },
            'requirements2.txt': {
                'pkgs': ['certifi==2020.6.20', 'chardet==3.0.4', 'elasticsearch==7.9.1', 'idna==2.10',
                         'requests==2.24.0', 'urllib3==1.25.10'],
                'files': ['requirements.txt']
            },
            'requirements3.txt': {
                'pkgs': ['test==1.0'],
                'files': []
            }
        }
        self.main_file_name = 'requirements.txt'

    def test_get_dir_requirements(self):
        root_dir = './tests_utils'
        self.assertEqual(get_dir_requirements(root_dir), self.requirements)

    def test_get_connected_files(self):
        excepted_result = sorted(['requirements.txt', 'requirements2.txt'])
        self.assertEqual(sorted(get_connected_files(self.requirements, self.main_file_name)), excepted_result)

    @mock.patch('src.requirements_extractor.os.path.basename', return_value='requirements.txt')
    @mock.patch('src.requirements_extractor.os.path.dirname', return_value='/')
    def test_extract_requirements(self, basename_mock, dirname_mock):
        connected_files = ['requirements.txt', 'requirements2.txt']
        pkgs = []
        pkgs.extend(self.requirements['requirements.txt']['pkgs'])
        pkgs.extend(self.requirements['requirements2.txt']['pkgs'])
        pkgs = sorted(pkgs)
        excepted_result = ','.join(pkgs)

        with mock.patch('src.requirements_extractor.get_dir_requirements', return_value=self.requirements) as mock_check:
            with mock.patch('src.requirements_extractor.get_connected_files', return_value=connected_files) as mock_check2:
                self.assertEqual(extract_requirements('requirements.txt'), excepted_result)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
