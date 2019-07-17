import os, sys

# Helper functions for wordify.py
def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

def replace_string_with_char_at_index(str, index, char):
    return str[:index] + char + str[index + 1:]
