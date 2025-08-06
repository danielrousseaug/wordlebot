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

        self.message = tk.Label(self, text='', font=("Helvetica", 14))
        self.message.grid(row=self.max_attempts+1, column=0, columnspan=5, padx=5, pady=5)

        self.bind('<Return>', lambda event: self.submit_guess())

    def submit_guess(self):
        if self.current_row >= self.max_attempts:
            return
        guess = self.entry.get().strip().lower()
        if len(guess) != 5 or guess not in self.words:
            self.message.config(text="Invalid word.", fg='red')
            return
        statuses = check_guess(guess, self.answer)

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
        elif self.current_row >= self.max_attempts:
            self.message.config(text=f'Game Over! The word was {self.answer.upper()}.', fg='red')
            self.entry.config(state='disabled')
            self.submit_btn.config(state='disabled')

def main():
    app = WordleGUI()
    app.mainloop()

if __name__ == '__main__':
    main()
