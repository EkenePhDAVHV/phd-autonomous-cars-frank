import os


class FileHandler:

    def __init__(self, directory='output'):
        # Init Data
        self.directory = self.fix_directory(directory)
        self.files = []

        # Create Directory
        if not os.path.isdir(directory):
            os.mkdir(directory)
        self.update_files()

    @staticmethod
    def fix_directory(directory):
        if not directory.endswith('/'):
            directory += '/'
        return directory

    def update_files(self):
        self.files = os.listdir(self.directory)

    def list_files(self, display=False):
        self.update_files()
        if display:
            for file in self.files:
                print(file)
        return self.files

    def write_file(self, filename='', file_contents='', sub_directory=''):
        _file = open(self.directory + self.fix_directory(sub_directory) + filename, 'w')
        _file.write(file_contents)

    def remove_files(self, files, display=False):
        self.update_files()
        if files is None:
            files = self.files
        for file in files:
            if display:
                print('Menus ' + file)
            os.remove(file)
        self.update_files()
