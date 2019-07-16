from typing import List

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
    return []
