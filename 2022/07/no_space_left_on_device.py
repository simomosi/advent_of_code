'''
https://adventofcode.com/2022/day/7

Output
[1] Sum of total sizes is 1297683
[2] Total size of smallest directory to free enough space: 5756764
'''

class Directory:
    def __init__(self, name: str):
        self.name: str = name
        self.files: list[str] = []
        self.files_size: int = 0
        self.subdirectories: dict[str, Directory] = {}
        self.total_size = 0

    def add_file(self, filename: str, size: int) -> None:
        self.files_size += size
        self.files.append(filename)

    def add_dir(self, directory: "Directory") -> None:
        self.subdirectories[directory.name] = directory

    def get_subdirectory(self, name: str) -> "Directory":
        return self.subdirectories[name]

class FilesystemNavigator:
    def __init__(self, root):
        self.all_directories : list[Directory] = []
        self.directory_stack : list[Directory] = []
        self.root: Directory = root
        self.current_directory: Directory = root

    def cd(self, argument: str) -> None:
        match argument:
            case '..':
                return self._cd_back()
            case '/':
                return self._cd_root()
            case _:
                return self._cd_directory(argument)

    def _cd_directory(self, directory_name: str) -> None:
        directory = self.current_directory.get_subdirectory(directory_name)
        self.current_directory = directory
        self.directory_stack.append(directory)
        self.all_directories.append(directory)

    def _cd_root(self) -> None:
        self.current_directory = self.root
        self.directory_stack = [self.root]
        self.all_directories.append(self.root)

    def _cd_back(self) -> None :
        self.directory_stack.pop()
        self.current_directory = self.directory_stack[-1]

def compute_directories_size(current: Directory) -> int :
    directories_size = 0
    for d in current.subdirectories.values():
        directories_size += compute_directories_size(d)
    current.total_size = current.files_size + directories_size
    return current.total_size

def sum_sizes_below_threshold(directory_collection: list[Directory], threshold: int) -> int:
    return sum(d.total_size for d in directory_collection if d.total_size < threshold)

def get_smallest_above_threshold(directory_collection: list[Directory], threshold: int) -> int:
    return min([d.total_size for d in directory_collection if d.total_size >= threshold])

def main():
    root = Directory('/')
    fsn = FilesystemNavigator(root)
    with open('07/input.txt', 'r') as file:
        for line in file:
            match line.strip().split():
                case "$", "ls":             # $ ls
                    pass
                case "$", "cd", argument:   # $ cd / | $ cd .. | $ cd folder
                    fsn.cd(argument)
                case "dir", dirname:        # dir abc
                    directory = Directory(dirname)
                    fsn.current_directory.add_dir(directory)
                case size, filename:        # 123 file.txt
                    fsn.current_directory.add_file(filename, int(size))
                case other:
                    raise Exception('Unexpected line ', other)
    compute_directories_size(fsn.root)
    total_sum = sum_sizes_below_threshold(fsn.all_directories, 100_000)
    print(f"[1] Sum of total sizes is {total_sum}")

    total_space_available = 70_000_000
    free_space = total_space_available - fsn.root.total_size
    space_required = 30_000_000
    additional_space_required = space_required - free_space

    smallest = get_smallest_above_threshold(fsn.all_directories, additional_space_required)
    print(f"[2] Total size of smallest directory to free enough space: {smallest}")

if __name__ == '__main__':
    main()