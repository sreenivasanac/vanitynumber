from vanitynumber import wordify

# {'A': '2', 'B': '2', 'C': '2', 'D': '3', 'E': '3', 'F': '3', 'G': '4',
# 'H': '4', 'I': '4', 'J': '5', 'K': '5', 'L': '5', 'M': '6', 'N': '6',
# 'O': '6', 'P': '7', 'Q': '7', 'R': '7', 'S': '7', 'T': '8', 'U': '8',
# 'V': '8', 'W': '9', 'X': '9', 'Y': '9', 'Z': '9'}

def test_number_to_words():
    assert wordify.number_to_words("1-800-724-6837") == "1-800-PAINTER"
    assert wordify.number_to_words("1-800-265-5343") == "1-800-COLLEGE"
    assert wordify.number_to_words("18336684372") == "1-833-MOVIES2"

    # Combination of TWO words
    assert wordify.number_to_words("1-866-386-6481") == "1-866-FUNMIT1"
    assert wordify.number_to_words("1-866-568-3968") == "1-866-LOVEYOU"
    assert wordify.number_to_words("1-866-266-5233") == "1-866-COOLBEE"

def test_words_to_number():
    assert wordify.words_to_number("1-800-PAINTER") == "1-800-724-6837"
    assert wordify.words_to_number("1-866-COOLBEE") == "1-866-266-5233"
    assert wordify.words_to_number("1-866-LOVEYOU") == "1-866-568-3968"


def test_all_wordifications():
    wordifications = wordify.all_wordifications("1-800-266-5233")
    few_sample_expected = ["1-800-COOLBED", "1-800-COOKADD"]
    assert all(word in wordifications for word in few_sample_expected)
