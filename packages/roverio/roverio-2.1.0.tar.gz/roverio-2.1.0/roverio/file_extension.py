import argparse
import os


class FileExtensionCLI():
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='File Extension searches for all files in a path with the specified file extension.'
        )
        parser.add_argument(
            '-p',
            '--path',
            required=True,
            help='Where File Extension will search for files with the specified file extension.'
        )
        parser.add_argument(
            '-e',
            '--extension',
            required=True,
            help='The file extension to search a path for.'
        )
        parser.parse_args(namespace=self)

    def run(self):
        FileExtension.main(
            path=self.path,
            extension=self.extension,
        )


class FileExtension():
    @staticmethod
    def main(path, extension):
        """Run the tool and print results to console
        """
        files = FileExtension.search_file_extensions(path, extension)
        for filename in files:
            print(filename)

    @staticmethod
    def search_file_extensions(path, extension):
        """Search for files with a specific extension in the specified directory
        """
        dirs_to_ignore = [
            'node_modules',
            'vendor',
            '.git',
            '__pycache__',
            'build',
            'dist',
        ]
        file_extension_files = []
        for root, dirs, files in os.walk(path, topdown=True):
            dirs[:] = [directory for directory in dirs if directory not in dirs_to_ignore]
            for file in files:
                if file.endswith(extension):
                    file_extension_file = os.path.join(root, file)
                    file_extension_files.append(file_extension_file)
        return file_extension_files


def main():
    FileExtensionCLI().run()


if __name__ == '__main__':
    main()
