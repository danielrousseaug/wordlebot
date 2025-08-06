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
 
def auto_solve(answer, words, max_attempts=6):
    """
    Automatically solve the Wordle puzzle for the given answer.
    Returns the number of attempts taken to guess the answer,
    or None if it fails within max_attempts.
    """
    guesses = []
    statuses_list = []
    possible = list(words)
    for attempt in range(1, max_attempts + 1):
        # filter possible candidates based on previous feedback
        possible = [
            w for w in possible
            if all(check_guess(g, w) == st for g, st in zip(guesses, statuses_list))
        ]
        # compute letter-position frequency table
        freq = {ch: [0] * 5 for ch in 'abcdefghijklmnopqrstuvwxyz'}
        for w in possible:
            for i, ch in enumerate(w):
                freq[ch][i] += 1
        # score candidates and pick the highest scoring guess
        best_guess = None
        best_score = -1
        for w in possible:
            if w in guesses:
                continue
            score = sum(freq[ch][i] for i, ch in enumerate(w))
            if score > best_score:
                best_score = score
                best_guess = w
        if not best_guess:
            return None
        guess = best_guess
        statuses = check_guess(guess, answer)
        guesses.append(guess)
        statuses_list.append(statuses)
        if guess == answer:
            return attempt
    return None
