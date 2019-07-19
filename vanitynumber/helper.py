import os, sys

import re # regular expressions

# Helper functions for wordify.py
PHONE_NUMBER_REGEX = {}
PHONE_NUMBER_REGEX["US"] = '(1?)-?([0-9]{3})-?([0-9]{3})-?([0-9]{4})$'
# Example matching number "1-800-724-6837"
# Four control groups in the above Regex which we would be matching


VANITY_PHONE_NUMBER_REGEX = {}
VANITY_PHONE_NUMBER_REGEX["US"] = '(1?)-?([0-9]{3})-?([a-zA-Z0-9]{7,8})$'
# Example matching wordified_number "1-800-PAINTER"


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
            count_continous_chars += 1
        if count_continous_chars > max_continous_chars_in_word:
            max_continous_chars_in_word = count_continous_chars
        if not char.isalpha():
            count_continous_chars = 0
    return max_continous_chars_in_word

def get_digit_to_chars_list_mapping():
    # Returns mapping of digit to their corresponding List[Characters]
    # as Typed in T9 Mobile dictionary https://en.wikipedia.org/wiki/T9_(predictive_text)
    # {"2" => ['A', 'B', 'C'], "3" => ['D', 'E', 'F'], ......}
    digit_to_chars_list_map = {
        "1":"",
        "2":"ABC",
        "3":"DEF",
        "4":"GHI",
        "5":"JKL",
        "6":"MNO",
        "7":"PQRS",
        "8":"TUV",
        "9":"WXYZ",
        "0":"",
    }
    for digit, chars_map in digit_to_chars_list_map.items():
        digit_to_chars_list_map[digit] = list(chars_map)

    return digit_to_chars_list_map

def validate_phone_number_regex(phone_number, country_code):
    global PHONE_NUMBER_REGEX
    pattern = re.compile(PHONE_NUMBER_REGEX[country_code])
    match = pattern.match(phone_number)
    assert(match)
    return match

def validate_wordified_number_regex(wordified_number, country_code):
    global VANITY_PHONE_NUMBER_REGEX
    pattern = re.compile(VANITY_PHONE_NUMBER_REGEX[country_code])
    match = pattern.match(wordified_number)
    assert(match)
    return match

def validate_phone_number_basic(phone_number):
    assert type(phone_number) is str
    assert(len(phone_number) >= 2 and len(phone_number) <= 14)
    return True

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

def add_hyphen_notation(number):
    # Args: Trailing number, usually of 7 digits
    # Returns: hyphen added 4 digits from the last
    if number and "-" not in number:
        # list(number) does Not work for some reason!
        number_ = [digit for digit in number]
        # Add Hyphen only between TWO Digits, and Not between TWO characters
        if number_[-3].isdigit() and number_[-4].isdigit():
            number_.insert(-4, "-")
        number = "".join(number_)
    return number

def is_valid_word(char_prefix, dictionary_trie):
    if dictionary_trie.has_key(char_prefix):
        return True
    # Some combination of continous words should exist
    for index, _ in enumerate(char_prefix):
        if dictionary_trie.has_key(char_prefix[:index + 1]) and \
            dictionary_trie.has_key(char_prefix[index + 1:]):
            return True
    return False

def is_valid_word_or_prefix(char_prefix, dictionary_trie):
    if dictionary_trie.has_key(char_prefix):
        return True
    # Some combination of continous words should exist
    for index, _ in enumerate(char_prefix):
        if dictionary_trie.has_key(char_prefix[:index + 1]) and \
            dictionary_trie.has_subtrie(char_prefix[index + 1:]):
            return True
    return False
