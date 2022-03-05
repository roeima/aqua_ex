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


def dump_yml(filename, yml_dict):
    with open(filename, 'w') as fp:
        yaml.dump(yml_dict, fp)


def load_yml(filename):
    with open(filename, 'r') as fp:
        return yaml.safe_load(fp)


def get_key(config_pos, tokens):
    added_key_tokens = tokens.copy()
    added_key_tokens.append(str(config_pos))
    added_key = '.'.join(added_key_tokens)
    return added_key


def check_exists(key, yml_keys):
    if key in yml_keys:
        return True
    for k in yml_keys:
        if key in k:
            return True
    return False


def get_origin_value(flat_key, original_dict):
    x = original_dict
    tokens = flat_key.split('.')
    for token in tokens:
        if token.isdigit():
            print(token)
            x = x[int(token)]
        else:
            x = x[token]
    return x


def add_config(yml_filename, extra_config):
    original_yml = load_yml(filename=yml_filename)
    yml_flat = flatten(original_yml)

    for config_key, value in extra_config.items():
        tokens = config_key.split('.')

        if check_exists(config_key, yml_flat.keys()):
            origin_value = get_origin_value(config_key, original_yml)
            if isinstance(origin_value, list):
                config_pos = len(origin_value)
                added_key = get_key(config_pos, tokens)
                yml_flat[added_key] = value
            else:
                del yml_flat[config_key]
                old_key = get_key(0, tokens)
                print(tokens)
                added_key = get_key(1, tokens)
                yml_flat[old_key] = origin_value
                yml_flat[added_key] = value
        else:
            yml_flat[config_key] = value

    print(yml_flat)
    dump_yml(f"new-{yml_filename}", unflatten(yml_flat))


def main():
    yml_filename = 'file.yml'

    extra_config = {
        'metadata.labels.app': 'roei2',
        'metadata.labels.prod': True,
        'spec.predictors.componentSpecs.spec.containers.0.image': 'roei_Test'
    }

    add_config(yml_filename, extra_config)


if __name__ == '__main__':
    main()
