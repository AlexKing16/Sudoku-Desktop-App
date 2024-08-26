import random
import csv
import sys
import time
import tkinter as tk
from tkinter import messagebox
import webbrowser
from sudoku import Sudoku
FONT= ("Verdana", 12)
csv_out = "input.csv"
csv_in = "output.csv"
pipe = "pipe.txt"

# Controls switching of tkinter frames
class SudokuApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.resizable(self, False, False)
        tk.Tk.geometry(self, '550x500')
        tk.Tk.title(self, 'Sudoku')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for page in (HomePage, RulesPage, HelpPage, MakeNewPuzzlePage):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        page_label = tk.Label(self, text="Sudoku Puzzle Maker and Solver", font=FONT)
        page_label.pack(pady=20, padx=10)

        rules_button = tk.Button(self, text="Rules", command=lambda: controller.show_frame(RulesPage))
        rules_button.pack(pady=1)

        help_button2 = tk.Button(self, text="Help", command=lambda: controller.show_frame(HelpPage))
        help_button2.pack(pady=1)

        new_puzzle_button = tk.Button(self, text="Make a new puzzle", cursor='plus',
                                      command=lambda: controller.show_frame(MakeNewPuzzlePage))
        new_puzzle_button.pack(pady=1)


class RulesPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        page_label = tk.Label(self, text="Rules of Sudoku", font=FONT)
        page_label.pack(pady=10,padx=10)

        def sudoku_wiki_link(url):
            webbrowser.open_new_tab(url)

        rules = "Sudoku is a game played on a 9x9 grid that is subdivided into nine 3x3 subgrids.\n" \
                "The objective is to fill each row, column, and subgrid with the numbers 1 through 9 \n" \
                "without any repetitions. "

        rules_label = tk.Label(self, text=rules, font=FONT, justify='left')
        rules_label.pack(pady=10, padx=10)

        link = tk.Label(self, text="Sudoku wiki", font=FONT, fg="light blue", cursor="hand2", justify='left')
        link.bind("<Button-1>", lambda e: sudoku_wiki_link("https://en.wikipedia.org/wiki/Sudoku"))
        link_label = tk.Label(self, text="Learn more about Sudoku by following the"
                                         " link below to the Sudoku Wikipedia page", font=FONT, justify='left')
        link_label.pack()
        link.pack()
        home_button = tk.Button(self, text="Return Home", command=lambda: controller.show_frame(HomePage))
        home_button.pack(pady=20)


class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        page_label = tk.Label(self, text="Help", font=FONT)
        page_label.pack(pady=10, padx=10)

        rules = 'Rules: Selecting this option from the home screen takes you to a window\n' \
                'where you can read about the rules and objective of Sudoku.'
        rules_label = tk.Label(self, text=rules, font=FONT, justify='left')
        rules_label.pack(pady=10, anchor='w')

        generate_puzzle = 'Make a new puzzle: Selecting this option from the home screen takes you to a window\n' \
                          'where you can generate and play new sudoku puzzles. The numbers highlighted\nin green are ' \
                          'given to you, and you have to figure out which numbers go in the white boxes.\nYou can enter ' \
                          'numbers into the boxes using your keyboard,\nor the on-screen numpad using your mouse.'

        generate_puzzle_label = tk.Label(self, text=generate_puzzle, font=FONT, justify='left')
        generate_puzzle_label.pack(pady=10, anchor='w')
        home_button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        home_button.pack(pady=10)


class MakeNewPuzzlePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        home_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        home_button.grid(sticky='w', row=0, column=0)

        easy_puzzle_button = tk.Button(self, text="New Easy Puzzle", cursor='plus',
                                       command=lambda: self.generate_puzzle('2', [easy_puzzle_button, med_puzzle_button, hard_puzzle_button]))
        easy_puzzle_button.grid(sticky='w', row=1, column=0)

        med_puzzle_button = tk.Button(self, text="New Medium Puzzle", cursor='plus',
                                  command=lambda: self.generate_puzzle('3',[easy_puzzle_button, med_puzzle_button, hard_puzzle_button]))
        med_puzzle_button.grid(sticky='w', row=2, column=0)

        hard_puzzle_button = tk.Button(self, text="New Hard Puzzle", cursor='plus',
                                  command=lambda: self.generate_puzzle('4',[easy_puzzle_button, med_puzzle_button, hard_puzzle_button]))
        hard_puzzle_button.grid(sticky='w', row=3, column=0)

    def clear_frame(self):
        for widget in self.winfo_children():
            if widget.widgetName == 'entry' or widget.widgetName == 'label':
                widget.destroy()

    def make_board(self, solution, difficulty):
        with open(csv_out, 'w', newline='') as csv_file:
            csv_out_file = csv.writer(csv_file, delimiter=',')
            for row in solution:
                csv_out_file.writerow(row)
        with open(pipe, 'w') as run_file:
            run_file.write(difficulty)

        # Microservice puts new board in csv.in
        time.sleep(2)

        with open(csv_in, 'r', newline='') as new_puzzle:
            csv_reader = csv.reader(new_puzzle, delimiter=',')
            new_board = []
            for row in csv_reader:
                new_board.append(row)
        print(new_board)

        return new_board

    def generate_puzzle(self, difficulty, btn=None):
        if btn is not None:  # Change command of buttons after first puzzle to show pop up
                btn[0].config(command=lambda: self.new_puzzle_pop_up('2'))
                btn[1].config(command=lambda: self.new_puzzle_pop_up('3'))
                btn[2].config(command=lambda: self.new_puzzle_pop_up('4'))
        puzzle = Sudoku(3, 3, seed=random.randrange(sys.maxsize)).difficulty(0.5)
        solution = puzzle.solve().board
        new_board = self.make_board(solution, difficulty)

        def show_solution_pop_up():
            msg = messagebox.askyesno('Show Solution?', 'Forfeit and show the solution for this puzzle?')
            if msg:
                self.show_board(solution, solution_button)

        solution_button = tk.Button(self, text="Show Solution", cursor='plus', command=show_solution_pop_up)
        solution_button.grid(sticky='w', row=4, column=0)
        self.show_board(new_board)

    def new_puzzle_pop_up(self, difficulty):
        if difficulty == '2':
            diff_name = "easy"
        elif difficulty == '3':
            diff_name = "medium"
        elif difficulty == '4':
            diff_name = "hard"
        message = f'Start a new {diff_name} puzzle? Any progress on your current puzzle will be lost'
        msg = messagebox.askyesno('New puzzle?', message)
        if msg:
            self.generate_puzzle(difficulty)

    def show_board(self, puzzle, btn=None):
        if btn is not None:
            btn.config(state='disabled')

        # Buttons for on screen numpad
        one_button = tk.Button(self, text="1", command=lambda: button_num_insert(1))
        two_button = tk.Button(self, text="2", command=lambda: button_num_insert(2))
        three_button = tk.Button(self, text="3", command=lambda: button_num_insert(3))
        four_button = tk.Button(self, text="4", command=lambda: button_num_insert(4))
        five_button = tk.Button(self, text="5", command=lambda: button_num_insert(5))
        six_button = tk.Button(self, text="6", command=lambda: button_num_insert(6))
        seven_button = tk.Button(self, text="7", command=lambda: button_num_insert(7))
        eight_button = tk.Button(self, text="8", command=lambda: button_num_insert(8))
        nine_button = tk.Button(self, text="9", command=lambda: button_num_insert(9))

        self.clear_frame()

        def button_num_insert(num):
            focus = self.focus_get()
            try:
                focus.delete(0, 1)
                focus.insert(0, num)
            except:
                pass

        def check_input(user_entry):
            if user_entry.isdigit() and len(user_entry) == 1 and user_entry != '0':
                return True
            elif len(user_entry) == 0:
                return True
            else:
                return False

        # Draw Sudoku board
        grid_row = 4
        grid_col = 4
        row_offset = 0
        for row in range(13):
            col_offset = 0
            for col in range(13):

                if row == 0 or row == 4 or row == 8 or row == 12:
                    if col == 0:
                        row_offset += 1
                    if col == 0 or col == 4 or col == 8 or col == 12:
                        line_label = tk.Label(self, text='+')
                    else:
                        line_label = tk.Label(self, text='--')
                    line_label.grid(row=row + grid_row, column=col + grid_col)

                elif col == 0 or col == 4 or col == 8 or col == 12:
                    col_offset += 1
                    line_label = tk.Label(self, text='|')
                    line_label.grid(row=row + grid_row, column=col + grid_col)
                else:
                    puzzle_x = row - row_offset
                    puzzle_y = col - col_offset
                    if puzzle[puzzle_x][puzzle_y] != '0':
                        num_label = tk.Label(self, text=f'{puzzle[puzzle_x][puzzle_y]}', bg='pale green',
                                             width=1, fg='Black')
                        num_label.grid(row=row + grid_row, column=col + grid_col, padx=3, pady=3)
                    else:
                        box = tk.Entry(self, bg='White', width=1, fg='Black')
                        box.grid(row=row + grid_row, column=col + grid_col)
                        reg = self.register(check_input)
                        box.config(validate="key", validatecommand=(reg, '%P'))

        one_button.grid(sticky='e', row=9, column=19)
        two_button.grid(sticky='e', row=9, column=20)
        three_button.grid(sticky='e', row=9, column=21)
        four_button.grid(sticky='e', row=10, column=19)
        five_button.grid(sticky='e', row=10, column=20)
        six_button.grid(sticky='e', row=10, column=21)
        seven_button.grid(sticky='e', row=11, column=19)
        eight_button.grid(sticky='e', row=11, column=20)
        nine_button.grid(sticky='e', row=11, column=21)

app = SudokuApp()
app.mainloop()

