#!/usr/bin/env python3
import cProfile
import copy
import re

from collections import Counter
from words import Catalog, Game, Result, Status, Suggester

catalog = Catalog()
num_runs = 100


def run(num_runs):
    guess_history = []
    for i in range(num_runs):
        game = Game(catalog)
        suggester = Suggester(catalog)

        num_guesses = 0
        while True:
            guess = suggester.suggest() if num_guesses > 0 else "least"
            num_guesses += 1
            result = game.check(guess)

            if all([r.Status == Status.RIGHT for r in result]):
                guess_history.append(num_guesses)
                break
            else:
                suggester.process(result)

    return guess_history


if __name__ == "__main__":
    result = run(num_runs)

    run_avg = sum(result) / len(result)
    run_min = min(result)
    run_max = max(result)

    print(f"Avg: {run_avg}\tMin: {run_min}\tMax: {run_max}")
    print(Counter(result))
