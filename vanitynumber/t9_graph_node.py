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
        return (self.max_number_of_continous_chars_in_word < other.max_number_of_continous_chars_in_word) or \
            ((self.max_number_of_continous_chars_in_word == other.max_number_of_continous_chars_in_word) and \
                (self.number_of_chars_in_word < other.number_of_chars_in_word))

    def __eq__(self, other):
        return (self.number_of_chars_in_word == other.number_of_chars_in_word) and \
            (self.max_number_of_continous_chars_in_word == other.max_number_of_continous_chars_in_word)

    def __gt__(self, other):
        return self.max_number_of_continous_chars_in_word > other.max_number_of_continous_chars_in_word or \
            ((self.max_number_of_continous_chars_in_word == other.max_number_of_continous_chars_in_word) and \
                (self.number_of_chars_in_word > other.number_of_chars_in_word))
