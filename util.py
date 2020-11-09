import os
import json

from contextlib import suppress


def read_file_into_str(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()


def write_str_to_file(file_name, text):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(text)
        file.close()


def exit_if_true(condition, message, prefix='ERROR: '):
    if condition:
        print(prefix + message)
        exit(0)


def main():
    r = json.loads(read_file_into_str('temp.json'))
    # noinspection PyUnusedLocal
    status = None
    with suppress(KeyError, IndexError):
        status = r['newMediaItemResults'][0]['status']['message']
    print(status)


if __name__ == "__main__":
    main()
