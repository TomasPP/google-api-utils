import os


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


if __name__ == "__main__":
    pass
    # main()
