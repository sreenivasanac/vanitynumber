import os
from typing import List
import re

import pygtrie as trie
# https://github.com/google/pygtrie

from collections import deque
from . import helper


MAX_WORD_LENGTH_DICTIONARY = 7
MAX_NUMBER_DIGITS_WORDIFY = 7

is_dictionary_trie_populated = False
dictionary_trie = None

# US_PHONE_NUMBER_REGEX = '1?-?[0-9]{3}-?[0-9]{3}-?[0-9]{4}$'
US_PHONE_NUMBER_REGEX = '(1?)-?([0-9]{3})-?([0-9]{3})-?([0-9]{4})$'


def get_digit_to_chars_list_mapping():
    # Returns mapping of digit to their corresponding list of Characters
    # as Typed in T9 Mobile dictionary https://en.wikipedia.org/wiki/T9_(predictive_text)
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
    # {'A' => '2', 'B' => '2'....,'Z' => '9'}
    digit_to_chars_list_map = get_digit_to_chars_list_mapping()

    char_to_digit_mapping = {}

    for digit, chars_map in digit_to_chars_list_map.items():
        for char in chars_map:
            char_to_digit_mapping[char] = digit

    return char_to_digit_mapping


def populate_dictionary_trie():
    global is_dictionary_trie_populated
    global dictionary_trie

    if is_dictionary_trie_populated == True and dictionary_trie is not None:
        # To avoid re-populating the Trie if it has already been created in Memory
        return dictionary_trie

    # Trie datastructure for storing dictionary words and fast retrieval
    dictionary_trie = trie.Trie()

    # https://stackoverflow.com/a/6475407/3766839
    with open(os.path.join(helper.get_script_path(), "dictionary.txt"), "r") as file:
        for word in file:
            word = str(word.upper()).rstrip() # stripping trailing newline characters, and making uppercase
            if len(word) <= MAX_WORD_LENGTH_DICTIONARY:
                dictionary_trie[word] = True

    is_dictionary_trie_populated = True
    return dictionary_trie

class Node(object):
    def __init__(self, wordified_so_far, index_so_far, number_of_chars_in_word):
        self.wordified_so_far = wordified_so_far
        self.index_so_far = index_so_far
        self.number_of_chars_in_word = number_of_chars_in_word

    def __le__(self, other):
        return self.number_of_chars_in_word < other.number_of_chars_in_word

    def __eq__(self, other):
        return self.number_of_chars_in_word == other.number_of_chars_in_word

    def __gt__(self, other):
        return self.number_of_chars_in_word > other.number_of_chars_in_word

def find_words_from_numbers(number: str, dictionary_trie, digit_to_chars_list_map):
    # Input "7246874"
    # Output wordified String "PAINTER"
    number_of_digits = len(number)

    # Performing Breadth-first Search
    queue = deque([])
    queue.append(Node(number, 0, 0))

    words_from_numbers = []

    while(queue):
        curr_wordified_node = queue.popleft()
        curr_wordified = curr_wordified_node.wordified_so_far
        curr_index = curr_wordified_node.index_so_far

        if curr_index == number_of_digits:
            if dictionary_trie.has_key(curr_wordified[:curr_index+1]):
                words_from_numbers.append(curr_wordified_node)
            continue

        curr_digit = number[curr_index]
        curr_number_of_chars_in_word = curr_wordified_node.number_of_chars_in_word

        for char in digit_to_chars_list_map[curr_digit]:
            next_wordified_node = helper.replace_string_with_char_at_index(curr_wordified, curr_index, char)
            # Only if the prefix exists in the Trie are we going deeper in the Search
            # If there does NOT exist ANY word with the prefix so far
            # the search will NOT go to the next level.
            prefix = next_wordified_node[:curr_index]
            if len(prefix) < 3 or (dictionary_trie.has_subtrie(prefix) or dictionary_trie.has_key(prefix)):
                queue.append(Node(next_wordified_node, curr_index + 1, curr_number_of_chars_in_word + 1))

    return max(words_from_numbers).wordified_so_far


def number_to_words(phone_number: str) -> str:
    """
    Args:
    - phone_number: a string representing a US phone number
                    e.g. "1-800-724-6837", "8007246874", "800-724-6837"

                    Currently does Not support following such formats with
                    brackets or space or their combination
                    404 663 9270, (404)-663-9270


    Returns:
    - wordified_number: a string which has transformed part or all of the phone
                         number into a single "wordified" phone number that can be
                         typed on a US telephone
                         e.g. "1-800-PAINTER"
    """
    dictionary_trie = populate_dictionary_trie()
    digit_to_chars_list_map = get_digit_to_chars_list_mapping()

    assert type(phone_number) is str
    assert(len(phone_number) >= 2 and len(phone_number) <= 14)

    pattern = re.compile(US_PHONE_NUMBER_REGEX)
    match = pattern.match(phone_number)
    assert(match)

    # Take only the last MAX_NUMBER_DIGITS_WORDIFY digits
    initial_digits = match.group(1) + "-" + match.group(2)
    trailing_digits = match.group(3) + match.group(4)

    wordified = find_words_from_numbers(trailing_digits, dictionary_trie, digit_to_chars_list_map)

    wordified_phone_number = initial_digits + "-" + wordified
    # Output = "1-800" + "-" + "PAINTER"

    return wordified_phone_number

def words_to_number(wordified_number: str) -> str:
    """
    Args:
    - wordified_number: a string representing a "wordified" phone number
                        either part or whole phone number is "wordified"
                        e.g. "1-800-PAINTER"

    Returns:
    - phone_number: a string which represents the US phone number
                    corresponding to the given wordified phone number
                    typed on a US telephone
                    e.g. "1-800-724-6837"
    """

    VANITY_PHONE_NUMBER_REGEX = '(1?)-?([0-9]{3})-?([\w-]*)$'

    assert type(wordified_number) is str
    assert(len(wordified_number) >= 2 and len(wordified_number) <= 14)

    pattern = re.compile(VANITY_PHONE_NUMBER_REGEX)
    match = pattern.match(wordified_number)
    assert(match)

    # wordified is present in in the Third Pattern Match Group, the last Seven letters
    # For example "PAINTER" in "1-800-PAINTER"
    wordified = match.group(3)
    wordified = wordified.replace("-", "")

    initial_digits = match.group(1) + "-" + match.group(2)

    char_to_digit_mapping = get_char_to_digit_mapping()
    trailing_digits = ""
    for char in wordified:
        if char.isalpha():
            letter = char_to_digit_mapping[char]
        else:
            letter = char

        trailing_digits = trailing_digits + letter

    return initial_digits + "-" + trailing_digits[:3] + "-" + trailing_digits[3:]

def all_wordifications() -> List[str]:
    """
    Args:
    - phone_number: a string representing a US phone number
                    e.g. "1-800-724-6837"

    Returns:
    - combinations: List of all possible combinations of numbers and English
                    words in a phone number
                    e.g. ["1-800-PAINTER", ]
    """

    populate_dictionary_trie()


    return []
