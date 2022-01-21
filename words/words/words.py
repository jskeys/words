import copy
import itertools
import random
import re

from enum import IntEnum
from typing import List, NamedTuple


class Status(IntEnum):
    WRONG = 1
    MISPLACED = 2
    RIGHT = 3


class Result(NamedTuple):
    Letter: str
    Index: int
    Status: Status


class Catalog:
    """Manages a list of words"""

    def __init__(self, path="/usr/share/dict/words", length=5):
        self._word_path = path

        words = []
        with open(self._word_path) as f:
            for word in f:
                if re.match(fr"[a-z]{{{length}}}$", word) is not None:
                    words.append(word.strip())

        self._words = tuple(words)

    def filter_by_regexes(self, regexes, check_indexes=None):
        """Return the indices of all words that match at least one regex"""
        if check_indexes is None:
            check_indexes = list(range(len(self._words)))

        match_indexes = []
        for i in check_indexes:
            word = self._words[i]
            if any([re.match(r, word) is not None for r in regexes]):
                match_indexes.append(i)

        return match_indexes

    def get_words(self):
        return self._words

    def get_num_words(self):
        return len(self._words)


class Game:
    def __init__(self, catalog):
        self._secret_word = random.choice(catalog.get_words())

    def check(self, guess) -> List[Result]:
        word = list(self._secret_word)
        guess = list(guess)

        # Assume all guesses are wrong and fill in the correct ones
        results = [Result(l, i, Status.WRONG) for i, l in enumerate(guess)]

        for i, l in enumerate(guess):
            if l == word[i]:
                word[i] = ""
                guess[i] = "*"
                results[i] = Result(l, i, Status.RIGHT)

        for i, l in enumerate(guess):
            if l in word:
                results[i] = Result(l, i, Status.MISPLACED)
                word[word.index(l)] = ""
        return results


class Constraint:
    """Tracks letter constraints"""

    def __init__(self, letter, size=5):
        self.letter = letter
        self.min_occurences = 0

        self.known_indexes = set()
        self.possible_indexes = set(list(range(size)))

    def update(self, results):
        """Update constraint using `results`"""
        match_results = [r for r in results if r.Letter == self.letter]
        other_results = [r for r in results if r.Letter != self.letter]

        occurences = len([r for r in match_results if r.Status in (Status.RIGHT, Status.MISPLACED)])

        self.min_occurences = max(occurences, self.min_occurences)

        for r in match_results:
            if r.Status == Status.RIGHT:
                self.known_indexes.add(r.Index)
                self.possible_indexes.discard(r.Index)
            elif r.Status == Status.MISPLACED:
                self.possible_indexes.discard(r.Index)

        for r in other_results:
            if r.Status == Status.RIGHT:
                self.possible_indexes.discard(r.Index)

        return self


class Suggester:
    """Tracks results and suggests next guess"""

    def __init__(self, catalog, length=5):
        self._word_length = length
        self._constraints = {}

        self._catalog = catalog
        self._word_indexes = list(range(self._catalog.get_num_words()))

    def _update_results(self, results):
        # create a new letter constraint non-existent, then update all constraints
        for r in results:
            if r.Letter not in self._constraints.keys():
                self._constraints[r.Letter] = Constraint(r.Letter)

        for constraint in self._constraints.values():
            constraint.update(results)

    def _create_regexes(self):
        """Create a list of regular expressions"""
        base_regex = [""] * self._word_length

        wrong_letters = [l for l, c in self._constraints.items() if c.min_occurences == 0]
        wrong_letters_string = "[^" + "".join(wrong_letters) + "]"

        for letter, constraint in self._constraints.items():
            for i in constraint.known_indexes:
                base_regex[i] = letter

        # Aggregate misplaced letters and possible indexes
        letters = []
        indexes = []
        for c in self._constraints.values():
            for i in range(c.min_occurences - len(c.known_indexes)):
                letters.append(c.letter)
                indexes.append(c.possible_indexes)

        # Iterate over all misplaced letter combinations that don't duplicate an index
        regexes = []
        for p in itertools.product(*indexes):
            if len(p) == len(set(p)):
                regex = copy.copy(base_regex)
                for l, i in zip(letters, p):
                    regex[i] = l
                for i, l in enumerate(regex):
                    if l == "":
                        regex[i] = wrong_letters_string
                regex_str = "^" + "".join(regex) + "$"
                regexes.append(regex_str)

        return regexes

    def _reduce_word_catalog(self):
        regexes = self._create_regexes()
        self._word_indexes = self._catalog.filter_by_regexes(regexes, self._word_indexes)

    def process(self, result):
        self._update_results(result)
        self._reduce_word_catalog()

    def suggest(self):
        random_word_index = random.choice(self._word_indexes)
        return self._catalog.get_words()[random_word_index]
