"""
wordle_game.py - Core game logic for Wordle clone.
"""
import os
import random

def load_word_list():
    """
    Load the list of valid words from wordlist.txt in this directory.
    Returns:
        List[str]: list of lowercase 5-letter words.
    """
    path = os.path.join(os.path.dirname(__file__), 'wordlist.txt')
    with open(path, 'r') as f:
        words = [w.strip().lower() for w in f if w.strip()]
    return words

def choose_random_word(words):
    """
    Choose a random word from the provided list.
    """
    return random.choice(words)

def check_guess(guess, answer):
    """
    Compare a guess to the answer, returning status for each letter.

    Args:
        guess (str): the guessed word (5 letters).
        answer (str): the answer word (5 letters).

    Returns:
        List[str]: statuses: 'correct', 'present', or 'absent' for each letter.
    """
    guess = guess.lower()
    answer = answer.lower()
    statuses = ['absent'] * len(guess)
    answer_chars = list(answer)

    # First pass: mark correct letters
    for i, letter in enumerate(guess):
        if letter == answer_chars[i]:
            statuses[i] = 'correct'
            answer_chars[i] = None

    # Second pass: mark present letters
    for i, letter in enumerate(guess):
        if statuses[i] == 'correct':
            continue
        if letter in answer_chars:
            statuses[i] = 'present'
            answer_chars[answer_chars.index(letter)] = None

    return statuses
