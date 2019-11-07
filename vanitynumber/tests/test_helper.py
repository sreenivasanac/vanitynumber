import pytest
from vanitynumber import helper

def checkEqual(L1, L2):
    return len(L1) == len(L2) and sorted(L1) == sorted(L2)

def test_get_digit_to_chars_list_mapping():
    digit_to_chars_list_map = helper.get_digit_to_chars_list_mapping()
    assert checkEqual(digit_to_chars_list_map['2'], ['A', 'B', 'C'])
    assert checkEqual(digit_to_chars_list_map['9'], ['W', 'X', 'Y', 'Z'])

def test_get_char_to_digit_mapping():
    char_to_digit_mapping = helper.get_char_to_digit_mapping()
    assert char_to_digit_mapping['A'] == '2'
    assert char_to_digit_mapping['Z'] == '9'

def test_is_valid_phone_number():
    goodinputs = ["1-800-724-6837", "1-866-265-5343", "8661236789", "1-800-123-4567", "8003456789"]

    for goodinput in goodinputs:
        assert helper.is_valid_phone_number(goodinput, "US") is True

    badinputs = ["45-23-2344-12", "12345", ""]
    for badinput in badinputs:
        assert helper.is_valid_phone_number(badinput, "US") is False


def test_is_valid_word_or_prefix():
    expected_outputs = {
    "SUNDAY": True,
    "CAPTA": True, # prefix for CAPTAIN
    "FUNDA": True, # prefix for FUNDAMENTAL
    "FUNZL": False
    }
    for word, is_valid in expected_outputs.items():
        assert helper.is_valid_word_or_prefix(word) == is_valid

def test_find_all_valid_word_substrings():
    wordified_number = "FUNMIT1"
    valid_word_substrings = helper.find_all_valid_word_substrings(wordified_number)
    assert "FUN" in valid_word_substrings

def test_validate_vanity_number_regex():
    goodinputs = ["1-800-PAINTER", "1-866-FUNMIT1"]

    for goodinput in goodinputs:
        assert helper.is_valid_vanity_number(goodinput, "US") is True

    badinputs = ["123"]
    for badinput in badinputs:
        assert helper.is_valid_vanity_number(badinput, "US") is False
