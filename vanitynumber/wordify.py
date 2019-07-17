import os, sys
from typing import List

import pygtrie as trie
# https://github.com/google/pygtrie

MAX_WORD_LENGTH = 7

is_dictionary_trie_populated = False

def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

def populate_dictionary_trie():
    global is_dictionary_trie_populated

    if is_dictionary_trie_populated == True:
        # To avoid re-populating the Trie if it has already been created in Memory
        return

    # Trie datastructure for storing dictionary words and fast retrieval
    dictionary_trie = trie.Trie()

    # https://stackoverflow.com/a/6475407/3766839
    with open(os.path.join(get_script_path(), "dictionary.txt"), "r") as file:
        for word in file:
            word = str(word)
            if len(word) <= MAX_WORD_LENGTH:
                dictionary_trie[word] = True

    is_dictionary_trie_populated = True

def number_to_words(phone_number: str) -> str:
    """
    Args:
    - phone_number: a string representing a US phone number
                    e.g. "1-800-724-6837"

    Returns:
    - wordified_number: a string which has transformed part or all of the phone
                         number into a single "wordified" phone number that can be
                         typed on a US telephone
                         e.g. "1-800-PAINTER"
    """
    populate_dictionary_trie()


    return phone_number

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
    
    return wordified_number

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
