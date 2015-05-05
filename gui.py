from   Tkinter import *
from   sudoku  import RecursiveBoard

import sys

class Sudoku(object):

    INPUT   = 1
    OUTPUT  = 3

    
    def __init__(self, rootWidget, board):
        self._rootWidget  = rootWidget
        self._board       = board
        self._tiles       = [[j for j in range(9)] for i in range(9)]
        frame             = Frame(self._rootWidget)
        board             = self.createBoard()
        self._solveButton = Button(frame, text="Solve", command=self.solve)
        self._solveButton.pack(side = LEFT)
        frame.pack()
        

    def run(self):
        self._rootWidget.mainloop()

    
    def _setReadyToExit(self):
        self._solveButton.configure(text="Exit",
                                    state=ACTIVE,
                                    command=quit)
        self._solveButton.pack()
 

    def solve(self):
        self._lockTiles()
        self._solveButton.configure(text="Solving...", state=DISABLED)
        self._solveButton.update()
        for col in range(9):
            for row in range(9):
                try:
                    val = int(self._tiles[col][row].get())
                    self._board.tile(col, row, val)
                except:
                    self.reset(col, row)
        print(str(self._board))
        self._board.describeCompressed(sys.stderr)
        solutions = self._board.solve()
        print ["solutions : ", solutions] 
        if len(solutions) > 0:
            self._showSolutions(solutions)
        else:
            self._setReadyToExit()
        

    def refresh(self):
        for col in range(9):
            for row in range(9):
                self.reset(col, row)


    def reset(self, col, row):
        oldVal = str(self._board.tile(col, row))
        self.setTile(col, row, oldVal)
        

    def setTile(self, col, row, val):
        entry = self._tiles[col][row]
        entry.delete(0, END)
        entry.insert(0, str(val))
    

    def createBoard(self):
        frame = Frame(self._rootWidget, relief=SUNKEN, bd=1)
        for x in range(3):
            for y in range(3):
                self.createBoardlet(frame, x, y)
        frame.pack()
        return frame

    
    def createBoardlet(self, parent, x, y):
        frame = Frame(parent, relief=SUNKEN, bd=1, padx=5, pady=5)
        vcmd  = (self._rootWidget.register(self._validateInput), '%P')
        for c in range(3):
            for r in range(3):
                xCoord = x * 3 + c
                yCoord = y * 3 + r
                entry  = Entry(frame, width=1, validate="key", validatecommand=vcmd)
                entry.insert(0, self._board.tile(xCoord, yCoord)) 
                entry.grid(column=c, row=r)
                self._tiles[xCoord][yCoord] = entry
        frame.grid(column=x, row=y)
        return frame


    def _validateInput(self, a):
        if a == '' or a == '.':
            return True
        try:
            ival = int(a)
            return True if 1 <= ival <= 9 else False
        except:
            return False


    def _lockTiles(self):
        for col in range(9):
            for row in range(9):
                entry = self._tiles[col][row]
                entry.configure(state=DISABLED)
                entry.update()


    def _setBoard(self, board):
        self._board = board
        for col in range(9):
            for row in range(9):
                entry = self._tiles[col][row]
                entry.configure(state=NORMAL)
                entry.update()
                self.reset(col, row)
                entry.configure(state="readonly")
                entry.update()

    
    def _showSolutions(self, solutions):

        def showNextSolution():
            if len(solutions) <= 0:
                self._setReadyToExit()
            else:
                self._setBoard(solutions.pop())

        self._solveButton.configure(text="Next Solution",
                                    state=ACTIVE,
                                    command=showNextSolution)
        self._solveButton.pack()
        showNextSolution()
    

if __name__ == '__main__':            
    board = RecursiveBoard()
    main  = Sudoku(Tk(), board)
    board.setPrintCycle(1000000)    
    main.run()

