# Wordle Clone

This is a clone of the Wordle game with both command-line (CLI) and graphical (GUI) interfaces.

## Requirements
- Python 3.x
- tkinter (for GUI version)

## Word List
The `wordlist.txt` file contains valid 5-letter words (one per line). You can extend or replace it as desired.

## Usage
First, change into the `wordle` directory:
```bash
cd wordle
```

### CLI Version
Run the command-line version:
```bash
python3 wordle_cli.py
```

### GUI Version
Run the graphical version:
```bash
python3 wordle_gui.py
```
 
### Auto Solver (GUI)
In the graphical version, click the **Auto Solve** button to have the game solve the current puzzle automatically. The solver uses a simple letter-position frequency heuristic:

- Maintains a list of possible candidate words consistent with all previous guesses and their feedback (correct, present, absent).
- For each candidate word, computes a score by summing the frequencies of its letters at their respective positions among the current candidate list.
- Selects the highest-scoring word as the next guess, applies it, receives feedback, and filters the candidate list accordingly.
- Repeats this process until the puzzle is solved or the maximum number of attempts is reached.

The Auto Solver can be invoked at any point (even mid-game) and will respect any manual guesses already entered.
