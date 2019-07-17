import os, sys

# Helper functions for wordify.py

def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

def replace_string_with_char_at_index(str, index, char):
    return str[:index] + char + str[index + 1:]

def find_char_prefix(word, index):
    # Returns the prefix length of contiguous characters ENDING AT THE GIVEN INDEX
    # For example word = "123RIDE4", index = 6
    # Will return prefix_length = 4  (char_prefix "RIDE" ends at index=6)
    char_prefix = ""
    while(index>=0 and word[index].isalpha()):
        char_prefix = word[index] + char_prefix
        index -= 1
    return char_prefix

def find_max_number_of_continous_chars_in_words(word):
    max_continous_chars_in_word = 0
    count_continous_chars = 0
    for char in word:
        if char.isalpha():
            count_continous_chars = count_continous_chars + 1
        else:
            if count_continous_chars > max_continous_chars_in_word:
                max_continous_chars_in_word = count_continous_chars
            count_continous_chars = 0
    return max_continous_chars_in_word

def get_digit_to_chars_list_mapping():
    # Returns mapping of digit to their corresponding List[Characters]
    # as Typed in T9 Mobile dictionary https://en.wikipedia.org/wiki/T9_(predictive_text)
    # {"2" => ['A', 'B', 'C'], "3" => ['D', 'E', 'F'], ......}
    digit_to_chars_list_map = {
        "2":"ABC",
        "3":"DEF",
        "4":"GHI",
        "5":"JKL",
        "6":"MNO",
        "7":"PQRS",
        "8":"TUV",
        "9":"WXYZ"
    }
    for digit, chars_map in digit_to_chars_list_map.items():
        digit_to_chars_list_map[digit] = list(chars_map)

    return digit_to_chars_list_map


def get_char_to_digit_mapping():
    # Returns corresponding digit for each character when typed in a phone
    # {'A' => '2', 'B' => '2',....,'Z' => '9'}
    # Reverse of the function get_digit_to_chars_list_mapping()
    digit_to_chars_list_map = get_digit_to_chars_list_mapping()

    char_to_digit_mapping = {}

    for digit, chars_map in digit_to_chars_list_map.items():
        for char in chars_map:
            char_to_digit_mapping[char] = digit

    return char_to_digit_mapping
