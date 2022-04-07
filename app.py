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
            self.w1.geometry('460x510')
        else:
            self.w1 = Frame(parent)
            self.w1.place(x=0, y=0, width=460, height=510)
        self.button1 = Button(self.w1, text="Open File", font=tkinter.font.Font(family="MS Shell Dlg 2", size=7),
                              cursor="arrow", state="normal")
        self.button1.place(x=330, y=20, width=120, height=32)
        self.button1['command'] = self.solve
        self.label3 = Label(self.w1, text="Open your sudoku's problem as txt file",
                            font=tkinter.font.Font(family="Segoe UI Variable Small Semibol", size=10), cursor="arrow",
                            state="normal")
        self.label3.place(x=10, y=20, width=320, height=32)
        self.label4 = Label(self.w1, text="Binomal Encoding",
                            font=tkinter.font.Font(family="Segoe UI Variable Small", size=14), cursor="arrow",
                            state="normal")
        self.label4.place(x=10, y=100, width=420, height=42)
        self.label4_copy = Label(self.w1, text="Sequential Encounter Encoding",
                                 font=tkinter.font.Font(family="Segoe UI Variable Small", size=14), cursor="arrow",
                                 state="normal")
        self.label4_copy.place(x=10, y=260, width=420, height=42)
        self.label5 = Label(self.w1, text="Number of variables: ",
                            font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label5.place(x=10, y=150, width=130, height=32)
        self.label6 = Label(self.w1, text="Number of clause: ",
                            font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label6.place(x=10, y=180, width=130, height=32)
        self.label7 = Label(self.w1, text="Time solving: ",
                            font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label7.place(x=10, y=210, width=130, height=32)
        self.label8 = Label(self.w1, text="Number of variables: ",
                            font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label8.place(x=10, y=310, width=130, height=32)
        self.label9 = Label(self.w1, text="Number of clause: ",
                            font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label9.place(x=10, y=340, width=130, height=32)
        self.label10 = Label(self.w1, text="Time solving: ",
                            font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label10.place(x=10, y=370, width=130, height=32)
        self.binomalNumClause = StringVar()
        self.binomalNumClause.set('')
        self.label11 = Label(self.w1, textvariable=self.binomalNumClause,
                            font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label11.place(x=130, y=180, width=50, height=32)
        self.binomalVariables = StringVar()
        self.binomalVariables.set('')
        self.label12 = Label(self.w1, textvariable=self.binomalVariables,
                            font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label12.place(x=130, y=150, width=50, height=32)
        self.binomalTime = StringVar()
        self.binomalTime.set('')
        self.label13 = Label(self.w1, textvariable=self.binomalTime,
                            font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label13.place(x=130, y=210, width=70, height=32)
        self.SEENumClause = StringVar()
        self.SEENumClause.set('')
        self.label14 = Label(self.w1, textvariable=self.SEENumClause,
                             font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label14.place(x=130, y=340, width=50, height=32)
        self.SEENumVariable = StringVar()
        self.SEENumVariable.set('')
        self.label15 = Label(self.w1, textvariable=self.SEENumVariable,
                             font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label15.place(x=130, y=310, width=50, height=32)
        self.SEETime = StringVar()
        self.SEETime.set('')
        self.label16 = Label(self.w1, textvariable=self.SEETime,
                             font=tkinter.font.Font(family="MS Shell Dlg 2", size=7), cursor="arrow", state="normal")
        self.label16.place(x=130, y=370, width=70, height=32)
        self.label17 = Label(self.w1, text="Open 'out.txt' to see the solution",
                             font=tkinter.font.Font(family="Segoe UI Variable Small Semibol", size=14), cursor="arrow",
                             state="normal")
        self.label17.place(x=10, y=450, width=400, height=32)

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
        grid_1 = []
        for i in range(0, 9):
            a = []
            for j in range(0, 10):
                tmp = data.read(1)
                if tmp != '\n' and tmp != '':
                    a.append(int(tmp))
            grid_1.append(a)

        grid_2 = grid_1

        def value(i, j, d):
            return 9 * (9 * (i - 1) + (j - 1)) + d

        def bi_normal():
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

                # Print number of variables in Binomial's case
                self.binomalVariables.set(str(729))

                # Print number SAT clause
                numclause = len(clauses)
                self.binomalNumClause.set(str(numclause))

                # solve the SAT problem
                start = time.time()
                sol = set(pycosat.solve(clauses))
                end = time.time()

                # print solving time
                self.binomalTime.set(str(round((end - start) * 1000, 5)) + " (ms)")

                def read_cell(i, j):
                    # return the digit of cell i, j according to the solution
                    for d in range(1, 10):
                        if value(i, j, d) in sol:
                            return d

                for i in range(1, 10):
                    for j in range(1, 10):
                        grid[i - 1][j - 1] = read_cell(i, j)

            solve_clause(grid_1)

        def sequential_encounter():
            # Reduces Sudoku problem to a SAT clauses
            def sudoku_clauses():
                res = []
                add = 729

                def valid(cells):
                    for d in range(1, 10):
                        for pos in range(0, 9):
                            if pos == 0:
                                res.append([-value(cells[pos][0], cells[pos][1], d), value(cells[pos][0],
                                                                                           cells[pos][1], d) + add])
                            elif pos == 8:
                                res.append([-value(cells[pos][0], cells[pos][1], d), -(value(cells[pos - 1][0],
                                                                                             cells[pos - 1][1],
                                                                                             d) + add)])
                            else:
                                res.append([-value(cells[pos][0], cells[pos][1], d), value(cells[pos][0],
                                                                                           cells[pos][1], d) + add])
                                res.append([-(value(cells[pos - 1][0], cells[pos - 1][1], d) + add),
                                            value(cells[pos][0], cells[pos][1], d) + add])
                                res.append([-value(cells[pos][0], cells[pos][1], d), -(value(cells[pos - 1][0],
                                                                                             cells[pos - 1][1],
                                                                                             d) + add)])

                # for all cells, ensure that each cell:
                for i in range(1, 10):
                    for j in range(1, 10):
                        # denotes (at least) one of the 9 digits (1 clause)
                        res.append([value(i, j, d) for d in range(1, 10)])
                        # does not denote two different digits at once (36 clauses)
                        res.append([-value(i, j, 1), value(i, j, 1) + add])
                        for d in range(2, 9):
                            res.append([-value(i, j, d), value(i, j, d) + add])
                            res.append([-(value(i, j, d - 1) + add), value(i, j, d) + add])
                            res.append([-value(i, j, d), -(value(i, j, d - 1) + add)])
                        res.append([-value(i, j, 9), -(value(i, j, 8) + add)])

                add += 729
                # does not denote that two same digit at a row
                for i in range(1, 10):
                    valid([(i, j) for j in range(1, 10)])

                add += 729
                # does not denote that two same digit at a column
                for j in range(1, 10):
                    valid([(i, j) for i in range(1, 10)])

                add += 729
                # does not denote that two same digit at a 3x3 box
                for i in 1, 4, 7:
                    for j in 1, 4, 7:
                        valid([(i + k % 3, j + k // 3) for k in range(9)])

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

                # Print number of clauses in SEE encoding's case
                numclause = len(clauses)
                self.SEENumClause.set(str(numclause))

                # Print number of variables in SEE encoding's case
                self.SEENumVariable.set(str(729 + (729 - 1)*4))

                # solve the SAT problem
                start = time.time()
                sol = set(pycosat.solve(clauses))
                end = time.time()

                # Print solving time in SEE encoding's case
                self.SEETime.set(str(round((end - start) * 1000, 5)) + " (ms)")

                def read_cell(i, j):
                    # return the digit of cell i, j according to the solution
                    for d in range(1, 10):
                        if value(i, j, d) in sol:
                            return d

                for i in range(1, 10):
                    for j in range(1, 10):
                        grid[i - 1][j - 1] = read_cell(i, j)

            solve_clause(grid_2)

        bi_normal()
        sequential_encounter()

        out_path = 'venv/out.txt'
        with open(out_path) as f:
            print(f.read())

        with open(out_path, mode='w') as f:
            for i in range(0, 9):
                for j in range(0, 9):
                    f.write(str(grid_1[i][j]) + ' ')
                f.write('\n')


a = Home(0)
a.w1.mainloop()
