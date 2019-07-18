import helper
import os
with open(os.path.join(helper.get_script_path(), "dictionary.txt"), "r") as file:
    file2 = (os.path.join(helper.get_script_path(), "dictionary_cleaned.txt"), "rb+")
    output = []
    for word in file:
        word = str(word.upper()).rstrip() # stripping trailing newline characters, and making uppercase
        if len(word) <= 2: # Save 1, 2 to 3 letter words and see if they are valid words, sanity clean them
            output.append(word)  # But TOO many non-useful words
        else:
            file2.write(word)
