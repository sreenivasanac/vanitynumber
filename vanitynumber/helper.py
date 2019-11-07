import os, sys

import re # regular expressions

import pygtrie as trie
# https://github.com/google/pygtrie

import yaml

# Helper functions for wordify.py
PHONE_NUMBER_REGEX = {}
PHONE_NUMBER_REGEX["US"] = '(1?)-?([0-9]{3})-?([0-9]{3})-?([0-9]{4})$'
# Example matching number "1-800-724-6837"
# Four control groups in the above Regex which we would be matching

VANITY_PHONE_NUMBER_REGEX = {}
VANITY_PHONE_NUMBER_REGEX["US"] = '(1?)-?([0-9]{3})-?([a-zA-Z0-9]{7,8})$'
# Example matching wordified_number "1-800-PAINTER"


is_dictionary_trie_populated = False
DICTIONARY_TRIE = None

MAX_WORD_LENGTH_DICTIONARY = 7
MAX_NUMBER_DIGITS_WORDIFY = 7
MIN_WORD_LENGTH_DICTIONARY = 3

def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

defaults = None
with open(os.path.join(get_script_path(), "defaults.yml"), 'r') as ymlfile:
    defaults = yaml.safe_load(ymlfile)

def replace_string_with_char_at_index(str, index, char):
    # Strings are immutable in python, hence this function
    return str[:index] + char + str[index + 1:]

def populate_dictionary_trie():
    global is_dictionary_trie_populated
    global DICTIONARY_TRIE

    if is_dictionary_trie_populated == True and DICTIONARY_TRIE is not None:
        # To avoid re-populating the Trie if it has already been created and populated inMemory
        return DICTIONARY_TRIE

    # Trie datastructure for storing dictionary words and fast retrieval, and prefix matching
    DICTIONARY_TRIE = trie.Trie()

    # https://stackoverflow.com/a/6475407/3766839
    with open(os.path.join(get_script_path(), "dictionary.txt"), "r") as file:
        for word in file:
            word = str(word.upper()).rstrip() # stripping trailing newline characters of words from file, and making uppercase

            # Not including 2 In-frequent Letter words since they are pretty random (LA, FR, etc) and give bad outputs
            if len(word) <= MAX_WORD_LENGTH_DICTIONARY and len(word) >= MIN_WORD_LENGTH_DICTIONARY:
                DICTIONARY_TRIE[word] = True

    is_dictionary_trie_populated = True
    return DICTIONARY_TRIE


def find_char_prefix(word, index):
    # Returns the prefix length of contiguous characters ENDING AT THE GIVEN INDEX
    # For example word = "123RIDE4", index = 6
    # Will return prefix_length = 4  (char_prefix "RIDE" ends at index=6)
    char_prefix = ""
    while(index>=0 and word[index].isalpha()):
        char_prefix = word[index] + char_prefix
        index -= 1
    return char_prefix

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

def get_phone_number_regex_groups(phone_number, country_code=defaults['country_code']):
    pattern = re.compile(PHONE_NUMBER_REGEX[country_code])
    match = pattern.match(phone_number)
    return match

def is_valid_phone_number(phone_number, country_code=defaults['country_code']):
    match = get_phone_number_regex_groups(phone_number, country_code)
    return bool(match)

def get_vanity_number_regex_groups(wordified_number, country_code=defaults['country_code']):
    pattern = re.compile(VANITY_PHONE_NUMBER_REGEX[country_code])
    match = pattern.match(wordified_number)
    return match

def is_valid_vanity_number(phone_number, country_code=defaults['country_code']):
    match = get_vanity_number_regex_groups(phone_number, country_code)
    return bool(match)

def validate_phone_number_basic(phone_number):
    assert type(phone_number) is str
    if not (len(phone_number) >= defaults['min_phone_length'] and len(phone_number) <= defaults['max_phone_length']):
        return False
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


def is_valid_word(char_prefix):
    # Returns True if the given wordified word is a Valid word,
    # either entirely or made up of substrings
    valid_word_substrings = find_valid_word_substrings(char_prefix)
    return len(valid_word_substrings) > 0

def find_valid_word_substrings(wordified_word):
    # Returns Valid words present in the given wordified word
    # either entire word or 2 or more dictionary words combined

    # "FUNDAY" -> ["FUN", "DAY"]
    # "COOL" -> ["COOL"]
    global DICTIONARY_TRIE
    populate_dictionary_trie()

    if DICTIONARY_TRIE.has_key(wordified_word):
        return [wordified_word]
    # Some combination of continous words should exist
    for index, _ in enumerate(wordified_word):
        if DICTIONARY_TRIE.has_key(wordified_word[:index + 1]) and \
            DICTIONARY_TRIE.has_key(wordified_word[index + 1:]):
            return [wordified_word[:index + 1], wordified_word[index + 1:]]

    return []

def is_valid_word_or_prefix(char_prefix):
    # "SUNDAY" -> "TRUE"
    # "CAPTA" -> "TRUE" (Prefix of "CAPTAIN")
    # "FUNDA" -> "TRUE" (Prefix of "FUN" + "DAY")
    # "FUNZL" -> "FALSE" (ZL is Not a prefix of any word)
    global DICTIONARY_TRIE
    populate_dictionary_trie()

    if DICTIONARY_TRIE.has_key(char_prefix) or DICTIONARY_TRIE.has_subtrie(char_prefix):
        return True
    # Some combination of continous words should exist
    for index, _ in enumerate(char_prefix):
        if DICTIONARY_TRIE.has_key(char_prefix[:index + 1]) and \
            DICTIONARY_TRIE.has_subtrie(char_prefix[index + 1:]):
            return True
    return False

def find_all_valid_word_substrings(wordified_number):
    # Returns all dictionary words present in the given wordified string
    # FUN9DAY => ["FUN", "DAY"]
    # MITFUN8 => ["MIT", "FUN"]
    # COOL123 => ["COOL"]

    all_substrings = []
    substring = ""
    len_word = len(wordified_number)
    for index, char in enumerate(wordified_number):
        if char.isalpha():
            substring += char
            if index == len_word - 1 or not wordified_number[index + 1].isdigit():
                all_substrings.append(substring)
        else:
            substring = ""
    return all_substrings

def evaluate_wordified_number(wordified_number):
    # Returns True if the Generated wordified number - has all valid dictionary words

    is_valid_wordified_phone_number = True
    max_length_word_substring = 0
    max_number_of_continous_chars_in_word = 0

    all_valid_word_substrings = find_all_valid_word_substrings(wordified_number)

    # If there are No characters or words in the number, then it is Not a valid Wordified number
    if len(all_valid_word_substrings) == 0:
        is_valid_wordified_phone_number = False
    else:
        for substring in all_valid_word_substrings:
            max_number_of_continous_chars_in_word = max(len(substring), max_number_of_continous_chars_in_word)
            valid_word_substrings = find_valid_word_substrings(substring)
            for valid_substring in valid_word_substrings:
                max_length_word_substring = max(len(valid_substring), max_length_word_substring)

    return (is_valid_wordified_phone_number, max_number_of_continous_chars_in_word, max_length_word_substring)
