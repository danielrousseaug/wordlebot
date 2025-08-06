#!/usr/bin/env python3
"""
wordle_cli.py - Command-line interface for Wordle clone.
"""
import sys
from wordle_game import load_word_list, choose_random_word, check_guess

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

def main():
    words = load_word_list()
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
