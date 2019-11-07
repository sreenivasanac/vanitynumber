import os
from typing import List
from collections import deque # For Queue
import heapq # For Priority Queue - Min Heap

from . import helper
from . import t9_graph_node

def find_words_from_numbers(number: str, max_number_results_to_output):
    """
    Args: Phone Number and max_number_results_to_output
    Returns: Wordified Numbers

    Example Input (number: "7246874", max_number_results_to_output=1)
    Example Output wordified String "PAINTER"

    Example Input (number: "2665233", max_number_results_to_output=10)
    Example Output wordified String ["COOLBED", "BOOKBEE", "COOKADD", "BOOLADD", ......]

    Returns [] or "" if No word can be formed, based on max_number_results_to_output > 1 or = 1
    """
    number_of_digits = len(number)

    digit_to_chars_list_map = helper.get_digit_to_chars_list_mapping()

    # Performing Breadth-first Search
    queue = deque([])
    queue.append(t9_graph_node.T9_Graph_Node(number, 0, 0, 0, 0))

    # Create an empty Max Heap
    words_from_numbers_pq = []
    # https://docs.python.org/2/library/heapq.html

    while(queue):
        curr_wordified_node = queue.popleft()
        curr_wordified = curr_wordified_node.wordified_so_far
        curr_index = curr_wordified_node.index_so_far

        # If the graph search reached the end of the number, then validate and push to results heap
        if curr_index == number_of_digits:

            (is_valid_wordified_phone_number, max_number_of_continous_chars_in_word, max_length_word_substring) = \
                helper.evaluate_wordified_number(curr_wordified)

            if not is_valid_wordified_phone_number:
                continue

            curr_wordified_node.max_number_of_continous_chars_in_word = max_number_of_continous_chars_in_word
            curr_wordified_node.max_length_word_substring = max_length_word_substring

            # Push the current element into priority queue
            heapq.heappush(words_from_numbers_pq, curr_wordified_node)
            # Have only total N elements in Priority Queue / Heap, and Remove other elements
            while len(words_from_numbers_pq) > max_number_results_to_output:
                heapq.heappop(words_from_numbers_pq)
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

            if ((char.isdigit() and (len_char_prefix == 0 or helper.is_valid_word(char_prefix))) or
                (char.isalpha() and (curr_index != number_of_digits - 1 and helper.is_valid_word_or_prefix(char_prefix+char))) or
                (char.isalpha() and (curr_index == number_of_digits - 1 and helper.is_valid_word(char_prefix+char)))):
                # Or if the current letter is a character, then the prefix so far should be present in the Trie,
                # only then we search one level down

                # Only if the prefix exists in the Trie are we going deeper in the Search
                # If there does NOT exist ANY word with the prefix so far
                # the search will NOT go to the next level.

                next_wordified_number = helper.replace_string_with_char_at_index(curr_wordified, curr_index, char)
                # print(next_wordified_number)
                next_number_chars_in_word = curr_number_of_chars_in_word + (1 if char.isalpha() else 0)
                (is_valid_wordified_phone_number, max_number_of_continous_chars_in_word, max_length_word_substring) = \
                    helper.evaluate_wordified_number(next_wordified_number)

                queue.append(t9_graph_node.T9_Graph_Node(next_wordified_number, curr_index + 1, \
                    next_number_chars_in_word, max_number_of_continous_chars_in_word, max_length_word_substring))

    # Returning the maximum T9_Graph_Node having most number of contigous letters, defined as the comparator function
    if len(words_from_numbers_pq) > 0:
        words_from_numbers_result = []

        nlargest_ = heapq.nlargest(max_number_results_to_output, words_from_numbers_pq)

        for wordified in nlargest_:
            words_from_numbers_result.append(wordified.wordified_so_far)

        return words_from_numbers_result[:max_number_results_to_output]
    else:
        return []


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
    helper.populate_dictionary_trie()

    is_valid_phone_number = helper.is_valid_phone_number(phone_number)
    match = helper.get_phone_number_regex_groups(phone_number, "US")

    # Take only the last MAX_NUMBER_DIGITS_WORDIFY digits
    initial_digits = ""
    if match.group(1): initial_digits += match.group(1) + "-"
    initial_digits += match.group(2)
    trailing_digits = match.group(3) + match.group(4)

    wordified = find_words_from_numbers(trailing_digits, 1)

    if not wordified:
        return ""

    # Select the first element of the returned results array as the most suitable element
    wordified = wordified[0]

    wordified_phone_number = initial_digits + "-" + wordified
    #                           "1-800" +     "-" +   "PAINTER"

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


    assert type(wordified_number) is str
    assert(len(wordified_number) >= 2 and len(wordified_number) <= 14)

    match = helper.get_vanity_number_regex_groups(wordified_number, "US")

    # wordified is present in in the Third Pattern Match Group, the last Seven letters
    # For example "PAINTER" in "1-800-PAINTER"
    wordified = match.group(3)
    wordified = wordified.replace("-", "")

    initial_digits = ""
    if match.group(1): initial_digits += match.group(1) + "-"
    initial_digits += match.group(2)

    char_to_digit_mapping = helper.get_char_to_digit_mapping()
    trailing_digits = ""
    for char in wordified:
        if char.isalpha():
            letter = char_to_digit_mapping[char]
        else:
            letter = char

        trailing_digits = trailing_digits + letter

    #       "1-800"         "-" +       "123"         + "-" +    "1234"
    return initial_digits + "-" + trailing_digits[:3] + "-" + trailing_digits[3:]


def all_wordifications(phone_number: str) -> List[str]:
    """
    Args:
    - phone_number: a string representing a US phone number
                    e.g. "1-800-724-6837"

    Returns:
    - wordifications: List of all possible combinations of numbers and English
                    words in a phone number
                    e.g. ["1-800-PAINTER", ...]
    """
    helper.populate_dictionary_trie()

    if not helper.is_valid_phone_number(phone_number, "US"):
        raise ValueError

    match = helper.get_phone_number_regex_groups(phone_number, "US")

    # Take only the last MAX_NUMBER_DIGITS_WORDIFY digits
    initial_digits = match.group(1) + "-" + match.group(2)
    trailing_digits = match.group(3) + match.group(4)

    wordifications = []
    wordifications = find_words_from_numbers(trailing_digits, max_number_results_to_output=100)

    for i, _ in enumerate(wordifications):
        wordifications[i] = helper.add_hyphen_notation(wordifications[i])
        wordifications[i] = initial_digits + "-" + wordifications[i]
    # Output = "1-800" + "-" + "PAINTER"
    return wordifications
