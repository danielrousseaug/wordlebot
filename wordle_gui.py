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
import tkinter.ttk as ttk

# Theme colors (Wordle-inspired dark mode)
BG_COLOR = "#121213"
EMPTY_BG = "#3a3a3c"
ABSENT_BG = "#787c7e"
PRESENT_BG = "#c9b458"
CORRECT_BG = "#6aaa64"
TEXT_COLOR = "#ffffff"
BUTTON_BG = "#565758"
BUTTON_FG = "#ffffff"
DELAY_MS = 800  # milliseconds between auto-solver steps

class WordleGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # set dark background
        self.configure(bg=BG_COLOR)
        self.title("Wordle Clone")
        self.resizable(False, False)
        # load word list and choose answer
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
        # prepare fonts
        grid_font = tkfont.Font(family="Helvetica", size=32, weight="bold")
        entry_font = tkfont.Font(family="Helvetica", size=16)

        # grid frame for letter cells
        self.grid_frame = tk.Frame(self, bg=BG_COLOR)
        self.grid_frame.grid(row=0, column=0, padx=10, pady=10)
        for row in range(self.max_attempts):
            row_labels = []
            for col in range(5):
                lbl = tk.Label(
                    self.grid_frame,
                    text='', font=grid_font,
                    width=4, height=2,
                    bg=EMPTY_BG, fg=TEXT_COLOR
                )
                lbl.grid(row=row, column=col, padx=3, pady=3)
                row_labels.append(lbl)
            self.grid_labels.append(row_labels)

        # control frame for entry and buttons
        self.control_frame = tk.Frame(self, bg=BG_COLOR)
        self.control_frame.grid(row=1, column=0, pady=(0,10))
        # configure ttk button style for dark theme
        style = ttk.Style(self)
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure(
            'Wordle.TButton',
            background=BUTTON_BG,
            foreground=BUTTON_FG,
            borderwidth=0,
            focusthickness=0,
            highlightthickness=0,
            padding=6,
        )
        style.map(
            'Wordle.TButton',
            background=[('active', BUTTON_BG)],
            foreground=[('active', BUTTON_FG)],
        )

        self.entry = tk.Entry(
            self.control_frame,
            font=grid_font, justify="center",
            bg=BG_COLOR, fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            width=6, borderwidth=2, relief="flat"
        )
        self.entry.grid(row=0, column=0, padx=(0,10))
        self.entry.focus()

        # Guess button with custom ttk style
        self.submit_btn = ttk.Button(
            self.control_frame,
            text="Guess",
            command=self.submit_guess,
            style="Wordle.TButton",
            width=8,
        )
        self.submit_btn.grid(row=0, column=1, padx=5)

        # Auto Solve button with custom ttk style
        self.auto_btn = ttk.Button(
            self.control_frame,
            text="Auto Solve",
            command=self.auto_solve,
            style="Wordle.TButton",
            width=10,
        )
        self.auto_btn.grid(row=0, column=2, padx=5)

        # status message label
        self.message = tk.Label(
            self, text='', font=entry_font,
            bg=BG_COLOR, fg=TEXT_COLOR
        )
        self.message.grid(row=2, column=0)

        # bind Enter key to guess submission
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

        # update grid cell colors
        for col, (letter, status) in enumerate(zip(guess.upper(), statuses)):
            lbl = self.grid_labels[self.current_row][col]
            lbl.config(text=letter)
            if status == 'correct':
                color = CORRECT_BG
            elif status == 'present':
                color = PRESENT_BG
            else:
                color = ABSENT_BG
            lbl.config(bg=color, fg=TEXT_COLOR)

        self.current_row += 1
        self.entry.delete(0, tk.END)
        self.message.config(text='')

        if guess == self.answer:
            self.message.config(text=f'You win! The word was {self.answer.upper()}.', fg=CORRECT_BG)
            self.entry.config(state='disabled')
            self.submit_btn.config(state='disabled')
            self.auto_btn.config(state='disabled')
        elif self.current_row >= self.max_attempts:
            self.message.config(text=f'Game Over! The word was {self.answer.upper()}.', fg=ABSENT_BG)
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
        # prepare candidates from solution list matching past feedback
        # prepare candidates matching past feedback
        self.solver_candidates = [
            w for w in self.words
            if all(check_guess(g, w) == st for g, st in zip(self.guesses, self.statuses_list))
        ]
        # start iterative solver with delay
        self.after(DELAY_MS, self._auto_step)

    def _auto_step(self):
        # stop if no attempts remain
        if self.current_row >= self.max_attempts:
            self.message.config(
                text=f'Auto solver: failed. The word was {self.answer.upper()}.',
                fg=ABSENT_BG
            )
            return
        possible = self.solver_candidates
        # compute position-frequency table
        freq = {ch: [0] * 5 for ch in 'abcdefghijklmnopqrstuvwxyz'}
        for w in possible:
            for i, ch in enumerate(w):
                freq[ch][i] += 1
        # score and select best candidate
        scored = []
        for w in possible:
            if w in self.guesses:
                continue
            score = sum(freq[ch][i] for i, ch in enumerate(w))
            scored.append((score, w))
        if not scored:
            self.message.config(text='Auto solver: no candidates remain.', fg=ABSENT_BG)
            return
        scored.sort(reverse=True)
        guess = scored[0][1]
        statuses = check_guess(guess, self.answer)
        # display guess
        for col, (letter, status) in enumerate(zip(guess.upper(), statuses)):
            lbl = self.grid_labels[self.current_row][col]
            lbl.config(text=letter)
            if status == 'correct':
                color = CORRECT_BG
            elif status == 'present':
                color = PRESENT_BG
            else:
                color = ABSENT_BG
            lbl.config(bg=color, fg=TEXT_COLOR)
        # record and advance
        self.guesses.append(guess)
        self.statuses_list.append(statuses)
        self.current_row += 1
        # refresh UI
        self.update_idletasks()
        # check success
        if guess == self.answer:
            self.message.config(
                text=f'Auto solver: solved in {self.current_row} attempts. The word was {self.answer.upper()}.',
                fg=CORRECT_BG
            )
            return
        # filter candidates and schedule next step
        self.solver_candidates = [
            w for w in possible
            if all(check_guess(g, w) == st for g, st in zip(self.guesses, self.statuses_list))
        ]
        self.after(DELAY_MS, self._auto_step)

def main():
    app = WordleGUI()
    app.mainloop()

if __name__ == '__main__':
    main()
