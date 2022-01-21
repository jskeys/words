#!/usr/bin/env python3
import re

from words import Catalog, Game, Result, Status, Suggester

status_map = {"=": Status.RIGHT, "x": Status.WRONG, "?": Status.MISPLACED}

if __name__ == "__main__":
    catalog = Catalog()
    suggester = Suggester(catalog)

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

        suggester.process(results)
        print("Try ", end="")
        print(suggester.suggest(), end=", ")
        print(len(suggester._word_indexes), end="")
        print(" words remain")
