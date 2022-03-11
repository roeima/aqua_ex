from yml_editor import YamlEditor


def main():
    editor = YamlEditor('file.yml')
    editor.save('new-file.yml')


if __name__ == '__main__':
    main()
