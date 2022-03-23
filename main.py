from src.requirements_extractor import extract_requirements
from src.yml_editor import YamlEditor


def edit_yml():
    editor = YamlEditor('yml_files/file.yml')
    extra_config = {
        'roei': 'roei_value',
        'roei2': [
            1, 2, 3, {'roei': 'roei'}
        ]
    }
    editor.add_config(extra_config)
    editor.save('yml_files/new-file.yml')


def extract():
    main_file = r'./req_files/requirements.txt'
    print(extract_requirements(main_file))


def main():
    edit_yml()
    extract()


if __name__ == '__main__':
    main()