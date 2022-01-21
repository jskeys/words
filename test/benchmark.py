#!/usr/bin/env python3
import re

from words import Catalog, Game, Result, Status, Suggester

NUM_GAMES = 100

if __name__ == "__main__":
    catalog = Catalog()
    game_summaries = []

    for i in range(NUM_GAMES):
        game = Game(catalog)
        suggester = Suggester()

        num_guesses = 0
        while True:
            guess = suggester.suggest() if num_guesses > 0 else "alone"
            num_guesses += 1
            result = game.check(guess)

            if all([r.Status == Status.RIGHT for r in result]):
                game_summaries.append(num_guesses)
                print(f"Word: {game._secret_word}\tResult: {guess}")
                break
            else:
                suggester.process(result)

        print(sum(game_summaries) / NUM_GAMES)
