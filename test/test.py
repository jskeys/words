#!/usr/bin/env python3
import re

from words import Catalog, Game, Result, Status, Suggester

status_map = {"=": Status.RIGHT, "x": Status.WRONG, "?": Status.MISPLACED}

if __name__ == "__main__":
    suggester = Suggester()

    while True:
        guess = input("Guess:  ")
        if re.match(r"^[a-z]{5}$", guess) is None:
            raise ValueError("Incorrect guess format.")

        check = input("Result: ")
        if re.match(r"^[=?x]{5}$", check) is None:
            raise ValueError("Incorrect result format.")

        results = []
        for i, (l, s) in enumerate(zip(guess, check)):
            results.append(Result(l, i, status_map[s]))

        print(suggester.suggest(results))
        print(len(suggester._catalog.get_words()))
