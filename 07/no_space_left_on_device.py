'''
https://adventofcode.com/2022/day/7

Output
[1] Sum of total sizes is 1297683
[2] Total size of smallest directory to free enough space: 5756764
'''

import re

command_cd_re = re.compile('\$ cd (.*)')
command_ls_line = '$ ls'
file_re = re.compile('(\d+) (\w+\.*\w*)')
dir_re = re.compile('dir (\w+)')

class Directory:
    def __init__(self, name: str):
        self.name: str = name
        self.files: list[str] = []
        self.files_size: int = 0
        self.subdirectories: dict[str, Directory] = {}
        self.total_size = 0

    def add_file(self, filename: str, size: int):
        self.files_size += size
        self.files.append(filename)

    def add_dir(self, directory: "Directory"):
        self.subdirectories[directory.name] = directory

    def get_subdirectory(self, name: str):
        return self.subdirectories[name]

class FilesystemNavigator:
    def __init__(self, root):
        self.all_directories : list[Directory] = []
        self.directory_stack : list[Directory] = []
        self.root: Directory = root
        self.current_directory: Directory = root

    def cd(self, argument: str):
        if argument == '..':
            return self._cd_back()
        if argument == '/':
            return self._cd_root()
        return self._cd_directory(argument)

    def _cd_directory(self, directory_name: str):
        directory = self.current_directory.get_subdirectory(directory_name)
        self.current_directory = directory
        self.directory_stack.append(directory)
        self.all_directories.append(directory)

    def _cd_root(self):
        self.current_directory = self.root
        self.directory_stack = [self.root]
        self.all_directories.append(self.root)

    def _cd_back(self):
        self.directory_stack.pop()
        self.current_directory = self.directory_stack[-1]

    def compute_size(self):
        return self._compute_size_recursive(self.root)

    def _compute_size_recursive(self, current: Directory):
        directories_size = 0
        for d in current.subdirectories.values():
            directories_size += self._compute_size_recursive(d)
        current.total_size = current.files_size + directories_size
        return current.total_size

def sum_size(directory_collection: list[Directory], limit: int) -> int:
    return sum(d.total_size for d in directory_collection if d.total_size < limit)

def get_smallest_above_threshold(directory_collection: list[Directory], threshold: int) -> int:
    return min([d.total_size for d in directory_collection if d.total_size >= threshold])

def main():
    root = Directory('/')
    fsn = FilesystemNavigator(root)
    with open('07/input.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line == command_ls_line: # ls
                pass
            elif re_result := command_cd_re.match(line): # cd
                argument = re_result.group(1)
                fsn.cd(argument)
            elif re_result := file_re.match(line): # 123 file.txt
                size, filename = re_result.groups()
                fsn.current_directory.add_file(filename, int(size))
            elif re_result := dir_re.match(line): # dir abc
                dirname = re_result.group(1)
                directory = Directory(dirname)
                fsn.current_directory.add_dir(directory)
            else:
                raise Exception('Unexpected line ', line)
    fsn.compute_size()
    total_sum = sum_size(fsn.all_directories, 100_000)
    print(f"[1] Sum of total sizes is {total_sum}")

    total_space_available = 70_000_000
    free_space = total_space_available - fsn.root.total_size
    space_required = 30_000_000
    additional_space_required = space_required - free_space

    smallest = min([d.total_size for d in fsn.all_directories if d.total_size >= additional_space_required])
    print(f"[2] Total size of smallest directory to free enough space: {smallest}")

if __name__ == '__main__':
    main()