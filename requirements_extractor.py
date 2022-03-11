import pkg_resources
import os


def get_dir_requirements(root_dir):
    dir_files = os.listdir(root_dir)
    dir_req_files = [file for file in dir_files if 'requirements' in file]
    requirements = {}
    for file in dir_req_files:
        with open(f"{root_dir}/{file}", 'r') as f:
            lines = f.readlines()
            pkgs_in_file = [str(requirment)
                            for requirment
                            in pkg_resources.parse_requirements(lines)]

            files = [file_name for file_name in [line.strip() for line in lines]
                     if 'requirements' in file_name and file_name in dir_req_files]

        pkgs_in_file = [pkg for pkg in pkgs_in_file if pkg not in files]
        requirements[file] = {
            'pkgs': pkgs_in_file,
            'files': files
        }
    return requirements


def get_connected_files(requirements, main_file_name):
    req_graph = {key: value['files'] for key, value in requirements.items()}
    connected_files = set()
    depth_first(req_graph, main_file_name, connected_files)
    return list(connected_files)


def depth_first(graph, current_vertex, visited):
    visited.add(current_vertex)
    for vertex in graph[current_vertex]:
        if vertex not in visited:
            depth_first(graph, vertex, visited)


def extract_requirements(main_file):
    main_file_name = os.path.basename(main_file)
    root_dir = os.path.dirname(os.path.abspath(main_file))
    requirements = get_dir_requirements(root_dir)
    connected_files = get_connected_files(requirements, main_file_name)

    pkgs = []
    for connected_file in list(connected_files):
        pkgs.extend(requirements[connected_file]['pkgs'])

    return ','.join(list(set(pkgs)))


def main():
    main_file = r'./req_files/requirements.txt'
    print(extract_requirements(main_file))


if __name__ == '__main__':
    main()
