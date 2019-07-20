# Phone Number Wordification

Module for "wordification" of Phone Numbers to create Vanity Numbers.
For example, the Toll Free Number "1-800-724-6837" could be wordified to "1-800-PAINTER"
for remembering easily.

## Approach and Algorithm used

Main files are [wordify.py](https://github.com/sreenivasanac/vanitynumber/blob/master/vanitynumber/wordify.py) and [helper.py](https://github.com/sreenivasanac/vanitynumber/blob/master/vanitynumber/helper.py)

The problem of search number of combinations of T9 predictive ways of generating Wordified numbers is approached by considering it as a graph problem, with Nodes representing possible combinations of characters for each digit, and Breadth first search is performed from the first digit to the end while checking for prefixes. Comparator function has been defined for `T9_Graph_Node` for performing comparative operations between graph Nodes like sorting, min, max, etc.

Since frequently while doing graph search, we need to check for prefix matching, and search for word if it is present in Dictionary, Trie Data structure is Used in this program for storing key value pairs for faster insertion and deletion. Dictionaries.txt is read and Trie Data Structure has been created and populated. Python Dictionary type could also have been used for this purpose, but it will Be more memory intensive to store in local memory while the program is running, and the program may crash for larger number of dictionary entries. Trie data structure can support larger dictionary sizes.

`Note`: The Trie data is being stored in a global variable, though using global variables are Not recommended in many cases, for persisting the file read, and to avoid re-computation (dictionary file read and Trie populate) between multiple functions, this approach is used. Will save considerable time if dictionary file is larger.

[`number_to_words`](https://github.com/sreenivasanac/vanitynumber/blob/master/vanitynumber/wordify.py#L109) -> Regex is used to compare phone numbers and fetch groups of area codes. Though for some scenarios it is recommended to avoid Regex, this usecase of fetching US phone number area codes looked more suitable for its use. Since US phone numbers can come in slightly different formats, to avoid writing complex and repeating logic for fetching groups of numbers in the US phone number, this approach is used.

The List of possible outputs are stored in Max Heap / Priority Queue for faster insertion and deletion queries and retrieving best N words, which is defined by comparator function (most number of English characters in wordified_number)

[`words_to_number`](https://github.com/sreenivasanac/vanitynumber/blob/master/vanitynumber/wordify.py#L147) -> After sanity validation, converts each character to its corresponding T9 digit based on defined hash map.
`
[`all_wordifications`](https://github.com/sreenivasanac/vanitynumber/blob/master/vanitynumber/wordify.py#L189) -> Same as number_to_words, returns more number of results, custom defined

Assumptions Made in this program:
1. There are many words in the dictionary which are NOT Useful (yo, ey, si, fr) and Needs data cleaning.
I've attempted to do data cleaning in data_cleaning.py but saved it for a later day.
Hence the program has IGNORED ALL TWO LETTER WORDS

2. The Approach currently considers only maximum of combination of TWO WORDS together, though it can be extended for more words.

## Getting Started

The VanityNumber module uses Most Popular 20,000 words in a dictionary 20k.txt taken from [google-10000-english](https://github.com/first20hours/google-10000-english)

It uses the following Libraries for Data Structure
[pygtrie](https://github.com/google/pygtrie) - Python library implementing a trie data structure

[heapq](https://docs.python.org/3.7/library/heapq.html) - Python library for implementing a Min Heap Priority Queue

[deque](https://docs.python.org/3.7/library/collections.html) - Deque for implementing a Queue Data-structure or Breadth first search

Main files are [wordify.py](https://github.com/sreenivasanac/vanitynumber/blob/master/vanitynumber/wordify.py) and [helper.py](https://github.com/sreenivasanac/vanitynumber/blob/master/vanitynumber/helper.py)

### Installing

Steps for installing in your development environment

```
virtualenv -p python3 <envname>

git clone https://github.com/sreenivasanac/vanitynumber
cd vanitynumber/
pip install -r requirements.txt
python setup.py install
```

### Usage
```
python

import vanitynumber

vanitynumber.number_to_words("1-866-386-6481")
>'1-866-FUNMIT1'

vanitynumber.words_to_number("1-800-724-6837")
>'1-866-COOLBEE'

vanitynumber.words_to_number("866-4FUNMIT")
>'866-438-6648'

vanitynumber.all_wordifications("1-800-266-5233")
>['1-800-BOOKBEE', '1-800-CNNJADE',...]
```

## Running the tests

```
pytest
```

## Authors

* [**Sreenivasan AC**](https://www.linkedin.com/in/sreenivasan-ac/)


## License

This project is licensed under EULA Restrictive License - see the [LICENSE](LICENSE) file for details
