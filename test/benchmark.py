#!/usr/bin/env python3
import cProfile
import copy
import re

from words import Catalog, Game, Result, Status, Suggester

catalog = Catalog()


def run():
    for i in range(10):
        game = Game(catalog)
        suggester = Suggester(catalog)

        num_guesses = 0
        while True:
            guess = suggester.suggest() if num_guesses > 0 else "alone"
            num_guesses += 1
            result = game.check(guess)

            if all([r.Status == Status.RIGHT for r in result]):
                print(f"Word: {game._secret_word}\tResult: {guess}")
                break
            else:
                suggester.process(result)


if __name__ == "__main__":
    cProfile.run("run()", sort="cumtime")
