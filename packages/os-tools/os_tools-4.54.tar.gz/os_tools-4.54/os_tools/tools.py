import os


###########################################################################
#
# this module meant to provide general handling to python files
#
###########################################################################


# will print an array
def print_arr(arr, divider='\n'):
    print(divider.join(arr))


# will ask the user for an input
def ask_for_input(question):
    return input(question + '\n')


# will copy to the clipboard
def copy_to_clipboard(text):
    import pyperclip
    pyperclip.copy(text)
    pyperclip.paste()


# will return the current text from the clipboard
def get_from_clipboard():
    import pyperclip
    return pyperclip.paste()


# will generate a random string /w letters, /w numbers and /w symbols in a given length
def generate_random_string(with_letters: bool, with_numbers: bool, with_symbols: bool, length):
    import random
    import string
    random_pattern = ""
    if with_letters:
        random_pattern += string.ascii_letters
    if with_numbers:
        random_pattern += string.digits
    if with_symbols:
        random_pattern += string.punctuation

    return ''.join([random.choice(random_pattern) for _ in
                    range(length)])


# will turn a hex to a rgb tuple (r, g, b)
def hex_to_rgb(hex_color):
    hex_tuple = hex_color.lstrip('#')
    return tuple(int(hex_tuple[i:i + 2], 16) for i in (0, 2, 4))


def rel_path_to_abs(rel_path, rel_path_start):
    """
    Will turn a relative path of a file to an absolute one (if this is an absolute path, the function will return it).

    Args:
       param rel_path: the relative path you want to turn to abs
       param rel_path_start: the path from which the rel path will be calculated
    """

    import os_file_handler.file_handler as fh

    # if that's a relative source
    if rel_path.startswith('./'):
        return rel_path_to_abs(os.path.join(fh.get_parent_path(rel_path_start), rel_path[2:]), rel_path_start)

    else:
        parent_num = rel_path.count('../')
        if parent_num > 0:
            parent_dir = fh.get_parent_path(rel_path_start)
            for i in range(0, parent_num):
                parent_dir = fh.get_parent_path(parent_dir)
            rest_of_path_idx = rel_path.rindex('../') + 3
            rest_of_path = rel_path[rest_of_path_idx:]
            return os.path.join(parent_dir, rest_of_path)
        else:
            return rel_path


# will run a command in the command line
def run_command(cmd):
    import os
    os.system(cmd)
