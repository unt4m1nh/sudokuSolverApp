import time
import pycosat

from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Combobox
from tkinter.ttk import Notebook
from tkinter import filedialog as fd
import tkinter.font


class Home():
    def __init__(self, parent):
        self.gui(parent)

    def gui(self, parent):
        if parent == 0:
            self.w1 = Tk()
            self.w1.geometry('460x610')
        else:
            self.w1 = Frame(parent)
            self.w1.place(x = 0, y = 0, width = 460, height = 610)
        self.button1 = Button(self.w1, text = "Open File",  font = tkinter.font.Font(family = "MS Shell Dlg 2", size = 7), cursor = "arrow", state = "normal")
        self.button1.place(x = 140, y = 540, width = 180, height = 52)
        self.button1['command'] = self.solve
        self.label1 = Label(self.w1, text = "  Click to open your *txt file", fg = "black", font = tkinter.font.Font(family = "MS Shell Dlg 2", size = 20), cursor = "arrow", state = "disabled")
        self.label1.place(x = 10, y = 30, width = 460, height = 72)
        self.text1 = Text(self.w1, font = tkinter.font.Font(family = "Courier New", size = 20, weight = "bold"), cursor = "arrow", state = "normal")
        self.text1.place(x = 40, y = 110, width = 380, height = 340)
        self.textVal = StringVar()
        self.textVal.set('')
        self.label2 = Label(self.w1, textvariable= self.textVal, fg = "#000000", font = tkinter.font.Font(family = "MS Shell Dlg 2", size = 20), cursor = "arrow", state = "normal")
        self.label2.place(x = 40, y = 470, width = 380, height = 52)

    def solve(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        data = open(filename)
        grid_to_solve = []
        for i in range(0, 9):
            a = []
            for j in range(0, 10):
                tmp = data.read(1)
                if tmp != '\n' and tmp != '':
                    a.append(int(tmp))
            grid_to_solve.append(a)

        def value(i, j, d):
            return 9 * (9 * (i - 1) + (j - 1)) + d

        # Reduces Sudoku problem to a SAT clauses
        def sudoku_clauses():
            res = []
            # for all cells, ensure that the each cell:
            for i in range(1, 10):
                for j in range(1, 10):
                    # denotes (at least) one of the 9 digits (1 clause)
                    res.append([value(i, j, d) for d in range(1, 10)])
                    # does not denote two different digits at once (36 clauses)
                    for d in range(1, 10):
                        for dp in range(d + 1, 10):
                            res.append([-value(i, j, d), -value(i, j, dp)])

            def valid(cells):
                for i, xi in enumerate(cells):
                    for j, xj in enumerate(cells):
                        if i < j:
                            for d in range(1, 10):
                                res.append([-value(xi[0], xi[1], d), -value(xj[0], xj[1], d)])

            # ensure rows and columns have distinct values
            for i in range(1, 10):
                valid([(i, j) for j in range(1, 10)])
                valid([(j, i) for j in range(1, 10)])

            # ensure 3x3 sub-grids "regions" have distinct values
            for i in 1, 4, 7:
                for j in 1, 4, 7:
                    valid([(i + k % 3, j + k // 3) for k in range(9)])

            # assert len(res) == 81 * (1 + 36) + 27 * 324
            return res

        def solve_clause(grid):
            # solve a Sudoku problem
            clauses = sudoku_clauses()
            for i in range(1, 10):
                for j in range(1, 10):
                    d = grid[i - 1][j - 1]
                    # For each digit already known, a clause (with one literal).
                    if d:
                        clauses.append([value(i, j, d)])

            # Print number SAT clause
            # numclause = len(clauses)
            # "P CNF " + str(numclause) + "(number of clauses)"

            # solve the SAT problem
            start = time.time()
            sol = set(pycosat.solve(clauses))
            end = time.time()

            # print("Time: " + str(end - start))
            self.textVal.set("Time: " + str(round(end - start, 4)) + " (s)")

            def read_cell(i, j):
                # return the digit of cell i, j according to the solution
                for d in range(1, 10):
                    if value(i, j, d) in sol:
                        return d

            for i in range(1, 10):
                for j in range(1, 10):
                    grid[i - 1][j - 1] = read_cell(i, j)

        solve_clause(grid_to_solve)
        for i in range(9):
            for j in range(9):
                self.text1.insert(INSERT, ' ' + str(grid_to_solve[i][j]))
            self.text1.insert(INSERT, '\n')


a = Home(0)
a.w1.mainloop()
