import pytest
from vanitynumber import helper

def test_get_digit_to_chars_list_mapping():
    digit_to_chars_list_map = helper.get_digit_to_chars_list_mapping()
    assert digit_to_chars_list_map['2'] == ['A', 'B', 'C']

def test_get_char_to_digit_mapping():
    char_to_digit_mapping = helper.get_char_to_digit_mapping()
    assert char_to_digit_mapping['A'] == '2'
    assert char_to_digit_mapping['Z'] == '9'

def test_validate_phone_number_regex():
    goodinputs = ["1-800-724-6837", "1-866-265-5343"]
    try:
        for goodinput in goodinputs:
            helper.validate_phone_number_regex(goodinput, "US")
    except AssertionError:
        pytest.fail("AssertionError..Regex Not Matched")

    with pytest.raises(AssertionError):
        badinputs = ["45-23-2344-12", "12345"]
        for badinput in badinputs:
            helper.validate_phone_number_regex(badinput, "US")
        pytest.fail("Expected AssertionError")
    # assert match.match("4046639270") == True


def test_is_valid_word_or_prefix():
    expected_outputs = {
    "SUNDAY": True,
    "CAPTA": True,
    "FUNDA": True,
    "FUNZL": False
    }
    for word, is_valid in expected_outputs.items():
        assert helper.is_valid_word_or_prefix(word) == is_valid


def test_find_all_valid_word_substrings():
    wordified_number = "FUNMIT1"
    valid_word_substrings = helper.find_all_valid_word_substrings(wordified_number)
    assert "FUN" in valid_word_substrings


def test_validate_phone_number_regex():
    goodinputs = ["1-800-PAINTER", "1-866-FUNMIT1"]
    try:
        for goodinput in goodinputs:
            helper.validate_wordified_number_regex(goodinput, "US")
    except AssertionError:
        pytest.fail("AssertionError..Regex Not Matched")

    badinputs = ["123"]
    with pytest.raises(AssertionError):
        for badinput in badinputs:
            helper.validate_wordified_number_regex(badinput, "US")
        pytest.fail("Expected AssertionError")
