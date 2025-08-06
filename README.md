# Wordle Implementation with Solver

This is a TKInter implementation of Worlde with an automatic solver. I've experimented with different solving techniques to reduce inference cost and this is the best I've managed.

## Requirements
- Python 3.x w/ tkinter

## Word List
The `wordlist.txt` file contains valid 5-letter words (one per line). You can extend or replace it as desired.

### CLI Version
Run the command-line version:
```bash
python3 wordle_cli.py
```

### Benchmark 

The CLI has benchmark to evaluate solver performance over multiple games.

Run the benchmark with:
```bash
python3 wordle_cli.py --benchmark
```
Use `-t N` or `--trials N` to specify the number of random games (default: 100), for example:
```bash
python3 wordle_cli.py --benchmark --trials 500
```

### GUI Version
Run the graphical version:
```bash
python3 wordle_gui.py
```
 
### Auto Solver (GUI)
In the graphical version, click the **Auto Solve** button to have the game solve the current puzzle automatically. The solver uses a  letter-position frequency heuristic:

- Maintains a list of possible candidate words consistent with all previous guesses and their feedback (correct, present, absent).
- For each candidate word, computes a score by summing the frequencies of its letters at their respective positions among the current candidate list.
- Selects the highest-scoring word as the next guess, applies it, receives feedback, and filters the candidate list accordingly.
- Repeats this process until the puzzle is solved or the maximum number of attempts is reached.

The Auto Solver can be invoked at any point (even mid-game) and will respect any manual guesses already entered.
