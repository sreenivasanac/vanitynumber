# Phone Number Wordification

Module for "wordification" of Phone Numbers to create Vanity Numbers.
For example, the Toll Free Number "1-800-724-6837" could be wordified to "1-800-PAINTER"
for remembering easily.

## Getting Started


The VanityNumber module uses Most Popular 20,000 words in a dictionary 20k.txt taken from [google-10000-english](https://github.com/first20hours/google-10000-english)

It uses Trie Library for faster dictionary lookup
[pygtrie](https://github.com/google/pygtrie) - Python library implementing a trie data structure

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

Steps for installing in your development environment

```
git clone https://github.com/sreenivasanac/vanitynumber
pip install -r requirements.txt
python setup.py install
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

```
pytest
```

## Authors

* **Sreenivasan AC** - *Initial work*


## License

This project is licensed under EULA Restrictive License - see the [LICENSE](LICENSE) file for details
