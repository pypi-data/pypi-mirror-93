import argparse
import os
import re


class SecretsCLI():
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Secrets searches a path for possible secrets in code.'
        )
        parser.add_argument(
            '-p',
            '--path',
            required=True,
            type=str,
            help='Where Secrets will search for the string specified in each file.'
        )
        parser.add_argument(
            '-l',
            '--length',
            default=16,
            type=int,
            help='The minimum length of the secrets to search for.'
        )
        parser.parse_args(namespace=self)

    def run(self):
        Secrets.main(
            path=self.path,
            length=self.length,
        )


class Secrets():
    @staticmethod
    def main(path, length):
        """Run the tool printing results to console
        """
        print('\n####################\nROVER IO - SECRETS\n####################\n')
        print('The following files may have secrets stored in them:\n')
        messages = Secrets.search_for_secrets(path, length)
        for message in messages:
            print(message)

    @staticmethod
    def search_for_secrets(path, length):
        """Search files for secrets such as passwords, API keys, etc
        """
        regex_pattern = re.compile(r'\b\w{' + str(length) + r',}\b')
        dirs_to_ignore = [
            'node_modules',
            'vendor',
            '.git',
            '__pycache__',
            'build',
            'dist',
            'htmlcov',
        ]
        if os.path.exists(os.path.join(path, '.gitignore')):
            gitignore = open(os.path.join(path, '.gitignore'), 'r').read().splitlines()
        else:
            gitignore = False

        # Run script iterating over each file and directory
        secrets_files = []
        for root, dirs, files in os.walk(path, topdown=True):
            dirs[:] = [directory for directory in dirs if directory not in dirs_to_ignore]
            for filename in files:
                if gitignore and filename in gitignore:
                    continue
                filepath = os.path.join(root, filename)

                # Open each file and print the findings
                with open(filepath, 'r', encoding='latin1') as single_file:
                    for line_number, line in enumerate(single_file, 1):
                        data = regex_pattern.findall(line)
                        for secret in data:
                            message = f'File: {filepath}\nSecret: {secret}\nLine: {line_number}\n'
                            secrets_files.append(message)
        return secrets_files


def main():
    SecretsCLI().run()


if __name__ == '__main__':
    main()
