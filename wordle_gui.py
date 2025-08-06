#!/usr/bin/env python3
"""
wordle_gui.py - Graphical interface for Wordle clone using tkinter.
"""
import sys
try:
    import tkinter as tk
    import tkinter.font as tkfont
except ImportError:
    print("Error: tkinter is required to run the GUI. Please install the tkinter package.")
    sys.exit(1)
from wordle_game import load_word_list, choose_random_word, check_guess

class WordleGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wordle Clone")
        self.resizable(False, False)
        self.words = load_word_list()
        self.answer = choose_random_word(self.words)
        self.current_row = 0
        self.max_attempts = 6
        # record of past guesses and their feedback statuses
        self.guesses = []
        self.statuses_list = []
        self.grid_labels = []
        self._setup_ui()

    def _setup_ui(self):
        font = tkfont.Font(family="Helvetica", size=32, weight="bold")
        for row in range(self.max_attempts):
            row_labels = []
            for col in range(5):
                lbl = tk.Label(self, text=' ', width=4, height=2, font=font,
                               borderwidth=2, relief="solid", bg="lightgray")
                lbl.grid(row=row, column=col, padx=5, pady=5)
                row_labels.append(lbl)
            self.grid_labels.append(row_labels)

        self.entry = tk.Entry(self, font=font, justify="center")
        self.entry.grid(row=self.max_attempts, column=0, columnspan=4, padx=5, pady=5)
        self.entry.focus()

        self.submit_btn = tk.Button(self, text="Guess", command=self.submit_guess)
        self.submit_btn.grid(row=self.max_attempts, column=4, padx=5, pady=5)
        # button to trigger automatic solver
        self.auto_btn = tk.Button(self, text="Auto Solve", command=self.auto_solve)
        self.auto_btn.grid(row=self.max_attempts, column=5, padx=5, pady=5)

        self.message = tk.Label(self, text='', font=("Helvetica", 14))
        # span across submit and auto-solve buttons as well
        self.message.grid(row=self.max_attempts+1, column=0, columnspan=6, padx=5, pady=5)

        self.bind('<Return>', lambda event: self.submit_guess())

    def submit_guess(self):
        if self.current_row >= self.max_attempts:
            return
        guess = self.entry.get().strip().lower()
        if len(guess) != 5 or guess not in self.words:
            self.message.config(text="Invalid word.", fg='red')
            return
        statuses = check_guess(guess, self.answer)
        # record this guess and feedback for solver
        self.guesses.append(guess)
        self.statuses_list.append(statuses)

        for col, (letter, status) in enumerate(zip(guess.upper(), statuses)):
            lbl = self.grid_labels[self.current_row][col]
            lbl.config(text=letter)
            if status == 'correct':
                lbl.config(bg='green', fg='white')
            elif status == 'present':
                lbl.config(bg='yellow', fg='black')
            else:
                lbl.config(bg='gray', fg='white')

        self.current_row += 1
        self.entry.delete(0, tk.END)
        self.message.config(text='')

        if guess == self.answer:
            self.message.config(text=f'You win! The word was {self.answer.upper()}.', fg='green')
            self.entry.config(state='disabled')
            self.submit_btn.config(state='disabled')
            self.auto_btn.config(state='disabled')
        elif self.current_row >= self.max_attempts:
            self.message.config(text=f'Game Over! The word was {self.answer.upper()}.', fg='red')
            self.entry.config(state='disabled')
            self.submit_btn.config(state='disabled')
            self.auto_btn.config(state='disabled')

    def auto_solve(self):
        """
        Automatically solve the puzzle using a simple letter-position frequency heuristic.
        Respects any previous guesses and their feedback.
        """
        # disable user input during auto-solve
        self.entry.config(state='disabled')
        self.submit_btn.config(state='disabled')
        self.auto_btn.config(state='disabled')
        # initialize candidate list based on past feedback
        possible = [w for w in self.words
                    if all(check_guess(g, w) == st for g, st in zip(self.guesses, self.statuses_list))]
        # solver loop
        while self.current_row < self.max_attempts:
            # compute letter-position frequencies
            freq = {ch: [0] * 5 for ch in 'abcdefghijklmnopqrstuvwxyz'}
            for w in possible:
                for i, ch in enumerate(w):
                    freq[ch][i] += 1
            # score candidates
            scored = []
            for w in possible:
                if w in self.guesses:
                    continue
                score = sum(freq[ch][i] for i, ch in enumerate(w))
                scored.append((score, w))
            if not scored:
                break
            scored.sort(reverse=True)
            guess = scored[0][1]
            statuses = check_guess(guess, self.answer)
            # display the guess in the UI
            for col, (letter, status) in enumerate(zip(guess.upper(), statuses)):
                lbl = self.grid_labels[self.current_row][col]
                lbl.config(text=letter)
                if status == 'correct':
                    lbl.config(bg='green', fg='white')
                elif status == 'present':
                    lbl.config(bg='yellow', fg='black')
                else:
                    lbl.config(bg='gray', fg='white')
            # record and advance
            self.guesses.append(guess)
            self.statuses_list.append(statuses)
            self.current_row += 1
            self.update()
            # check for success
            if guess == self.answer:
                self.message.config(
                    text=f'Auto solver: solved in {self.current_row} attempts. The word was {self.answer.upper()}.',
                    fg='green')
                return
            # filter for next round
            possible = [w for w in possible
                        if all(check_guess(g, w) == st for g, st in zip(self.guesses, self.statuses_list))]
        # end solver loop
        if self.current_row >= self.max_attempts:
            self.message.config(text=f'Auto solver: failed. The word was {self.answer.upper()}.', fg='red')
        else:
            self.message.config(text='Auto solver: no candidates remain.', fg='red')

def main():
    app = WordleGUI()
    app.mainloop()

if __name__ == '__main__':
    main()
