import pytest
from vanitynumber import wordify

def test_number_to_words():
    assert wordify.number_to_words("1-800-724-6837") == "1-800-PAINTER"

def test_words_to_number():
    assert wordify.number_to_words("1-800-PAINTER") == "1-800-724-6837"

def test_all_wordifications():
    assert len(wordify.all_wordifications()) > 0
