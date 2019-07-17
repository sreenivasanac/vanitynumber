import os
from typing import List
import re # regular expressions

import pygtrie as trie
# https://github.com/google/pygtrie

from collections import deque # For Queue
import heapq_max # For Priority Queue - Max Heap
from . import helper


MAX_WORD_LENGTH_DICTIONARY = 7
MAX_NUMBER_DIGITS_WORDIFY = 7

is_dictionary_trie_populated = False
dictionary_trie = None

US_PHONE_NUMBER_REGEX = '(1?)-?([0-9]{3})-?([0-9]{3})-?([0-9]{4})$'
# Four control groups in the above Regex which we would be matching


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

# Graph Node for T9 Dictionary Wordifier
class T9_Graph_Node(object):
    def __init__(self, wordified_so_far, index_so_far, number_of_chars_in_word, max_number_of_continous_chars_in_word):
        self.wordified_so_far = wordified_so_far
        self.index_so_far = index_so_far
        self.number_of_chars_in_word = number_of_chars_in_word
        self.max_number_of_continous_chars_in_word = max_number_of_continous_chars_in_word

    # Comparator functions, for sorting, and min, max
    # If both nodes contain same number of characters in the word, then compare max number of continous characters between them
    def __le__(self, other):
        return (self.number_of_chars_in_word > other.number_of_chars_in_word) or \
            ((self.number_of_chars_in_word == other.number_of_chars_in_word) and (self.max_number_of_continous_chars_in_word > other.max_number_of_continous_chars_in_word))

    def __eq__(self, other):
        return (self.number_of_chars_in_word == other.number_of_chars_in_word) and (self.max_number_of_continous_chars_in_word == other.max_number_of_continous_chars_in_word)

    def __gt__(self, other):
        return self.number_of_chars_in_word < other.number_of_chars_in_word or \
            ((self.number_of_chars_in_word == other.number_of_chars_in_word) and (self.max_number_of_continous_chars_in_word < other.max_number_of_continous_chars_in_word))

def find_words_from_numbers(number: str, digit_to_chars_list_map, number_results_to_output):
    # Input "7246874"
    # Output wordified String "PAINTER"
    number_of_digits = len(number)

    global dictionary_trie

    # Performing Breadth-first Search
    queue = deque([])
    queue.append(T9_Graph_Node(number, 0, 0, 0))

    words_from_numbers_pq = heapq_max.heapify_max([])

    words_from_numbers_pq = []

    while(queue):
        curr_wordified_node = queue.popleft()
        curr_wordified = curr_wordified_node.wordified_so_far
        curr_index = curr_wordified_node.index_so_far

        if curr_index == number_of_digits:
            # Push the current element into priority queue "Max Heap"
            heapq_max.heappush_max(words_from_numbers_pq, curr_wordified_node)

            # Have only N elements in Priority Queue / Heap, and Remove other elements
            while len(words_from_numbers_pq) > number_results_to_output:
                heapq_max.heappop_max(words_from_numbers_pq)
            continue

        curr_digit = number[curr_index]
        curr_number_of_chars_in_word = curr_wordified_node.number_of_chars_in_word

        # For finding Partial Wordification (1-800-724-BEER)
        # Calculate character prefix length ending at the index so far
        char_prefix = helper.find_char_prefix(curr_wordified, curr_index - 1)
        len_char_prefix = len(char_prefix)

        for char in (digit_to_chars_list_map[curr_digit] + [curr_digit]):

             # If the current letter is a DIGIT either there should be only digits running till this point,
             # or a valid word formed till this point,
             # only then we replace the next index of a running word to a digit
            if ((char.isdigit() and (len_char_prefix == 0 or dictionary_trie.has_key(char_prefix))) or
                (char.isalpha() and (dictionary_trie.has_subtrie(char_prefix+char) or dictionary_trie.has_key(char_prefix+char)))):
                # Or if the current letter is a character and the prefix so far is present in the Trie, we replace the next index with a character

                # Only if the prefix exists in the Trie are we going deeper in the Search
                # If there does NOT exist ANY word with the prefix so far
                # the search will NOT go to the next level.

                next_wordified_number = helper.replace_string_with_char_at_index(curr_wordified, curr_index, char)
                # print(next_wordified_number)
                next_number_chars_in_word = curr_number_of_chars_in_word + (1 if char.isalpha() else 0)
                max_number_of_continous_chars_in_word = helper.find_max_number_of_continous_chars_in_words(next_wordified_number)

                queue.append(T9_Graph_Node(next_wordified_number, curr_index + 1, next_number_chars_in_word, max_number_of_continous_chars_in_word))

    # Returning the maximum T9_Graph_Node having most number of contigous letters, defined as the comparator function
    if len(words_from_numbers_pq) > 0:
        words_from_numbers_output = []
        for i in range(number_results_to_output):
            words_from_numbers_output.append(heapq_max.heappop_max(words_from_numbers_pq).wordified_so_far)

        if number_results_to_output == 1:
            return words_from_numbers_output[0]
        else:
            return words_from_numbers_output
    else:
        return number


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
    global dictionary_trie
    populate_dictionary_trie()
    digit_to_chars_list_map = helper.get_digit_to_chars_list_mapping()

    assert type(phone_number) is str
    assert(len(phone_number) >= 2 and len(phone_number) <= 14)

    pattern = re.compile(US_PHONE_NUMBER_REGEX)
    match = pattern.match(phone_number)
    assert(match)

    # Take only the last MAX_NUMBER_DIGITS_WORDIFY digits
    initial_digits = match.group(1) + "-" + match.group(2)
    trailing_digits = match.group(3) + match.group(4)

    wordified = find_words_from_numbers(trailing_digits, digit_to_chars_list_map, 1)

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

    char_to_digit_mapping = helper.get_char_to_digit_mapping()
    trailing_digits = ""
    for char in wordified:
        if char.isalpha():
            letter = char_to_digit_mapping[char]
        else:
            letter = char

        trailing_digits = trailing_digits + letter

    return initial_digits + "-" + trailing_digits[:3] + "-" + trailing_digits[3:]

def all_wordifications(phone_number: str) -> List[str]:
    """
    Args:
    - phone_number: a string representing a US phone number
                    e.g. "1-800-724-6837"

    Returns:
    - combinations: List of all possible combinations of numbers and English
                    words in a phone number
                    e.g. ["1-800-PAINTER", ]
    """
    global dictionary_trie
    populate_dictionary_trie()
    find_words_from_numbers(number, digit_to_chars_list_map, number_results_to_output=10)

    return []
