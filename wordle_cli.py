#!/usr/bin/env python3
"""
wordle_cli.py - Command-line interface for Wordle clone.
"""
import sys
import argparse
from wordle_game import load_word_list, choose_random_word, check_guess, auto_solve

# ANSI color codes for CLI feedback
GREEN = '\033[1;42m'
YELLOW = '\033[1;43m'
GRAY = '\033[1;40m'
RESET = '\033[0m'

def print_guess(guess, statuses):
    """Print the guess with colored background for each letter."""
    output = []
    for letter, status in zip(guess.upper(), statuses):
        if status == 'correct':
            color = GREEN
        elif status == 'present':
            color = YELLOW
        else:
            color = GRAY
        output.append(f"{color}{letter}{RESET}")
    print(''.join(output))

def run_benchmark(words, trials, max_attempts=6):
    """Run auto solver benchmark over a number of random answers."""
    results = []
    for _ in range(trials):
        answer = choose_random_word(words)
        attempts = auto_solve(answer, words, max_attempts)
        results.append(attempts)
    solved = [r for r in results if r is not None]
    failed = len(results) - len(solved)
    if solved:
        avg = sum(solved) / len(solved)
        best = min(solved)
        worst = max(solved)
    else:
        avg = best = worst = None
    print(f'Benchmark results over {trials} trials:')
    print(f'  Solved: {len(solved)}, Failed: {failed}')
    if solved:
        print(f'  Average guesses (solved games): {avg:.2f}')
        print(f'  Best (fewest guesses): {best}')
        print(f'  Worst (most guesses): {worst}')
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Wordle CLI')
    parser.add_argument('-b', '--benchmark', action='store_true',
                        help='Run auto solver benchmark')
    parser.add_argument('-t', '--trials', type=int, default=100,
                        help='Number of trials for benchmark (default: 100)')
    args = parser.parse_args()

    words = load_word_list()
    if args.benchmark:
        run_benchmark(words, args.trials)

    answer = choose_random_word(words)
    attempts = 6
    for turn in range(1, attempts + 1):
        while True:
            guess = input(f'Guess {turn}/{attempts}: ').strip().lower()
            if len(guess) != 5:
                print('Please enter a 5-letter word.')
            elif guess not in words:
                print('Word not in list. Choose another.')
            else:
                break
        statuses = check_guess(guess, answer)
        print_guess(guess, statuses)
        if guess == answer:
            print(f'Congratulations! You guessed the word in {turn} attempts.')
            sys.exit(0)
    print(f'Sorry, you did not guess the word. The answer was: {answer.upper()}')

if __name__ == '__main__':
    main()
