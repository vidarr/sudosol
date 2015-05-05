import sys
import copy

INTERNAL_FREE = "."
FREE          = "" 
OCCUPIED      = "X"
INVALID       = "invalid"
MAX_ROW_INDEX = 8
MAX_COL_INDEX = 8


class BaseBoard(object):
    '''
    Provides basic functionality for a sudoku board.
    '''
    
    def __init__(self, **params):
        self._printCycle = 1000000
        self._iteration = 0
        self._iterationRaise = 0
        self._solutions = []
        if 'BOARD' in params:
            self.__board = params['BOARD'];
        else:
            self.__board = [INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,
                            INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,
                            INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,
                            INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,
                            INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,
                            INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,
                            INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,
                            INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,
                            INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE,  INTERNAL_FREE, INTERNAL_FREE, INTERNAL_FREE]


    def tile(self, x, y, content = INVALID):
        if content == INVALID:
            cont = self._access(x, y)
        elif 1 <= content <= 9:
            cont = self._access(x, y, content - 1)
        elif content == FREE:
            cont = self._access(x, y, INTERNAL_FREE)
        else:
            raise ValueError("invalid")
        return cont + 1 if 0 <= cont <= 8 else (FREE if cont == INTERNAL_FREE else cont)


    def setPrintCycle(self, cycle = -1):
        self._printCycle = cycle
        self._iterationRaise = 0 if cycle < 0 else 1


    def _access(self, x, y, content = INVALID):
        index = y * 9 + x
        if content != INVALID:
            self.__board[index] = content
        return self.__board[index]

    
    def describeCompressed(self, out):
        [out.write(str(self.__board[i])) for i in range(0, len(self.__board))]


    def clone(self):
        return BaseBoard(BOARD=[self.__board[i] for i in range(len(self.__board))])
    
    
    def __str__(self):
        result = ""
        for squareY in range(3):
            for row in [squareY * 3 + k for k in range(3)]: 
                for squareX in range(3):
                    for col in [squareX * 3 + k for k in range(3)]:
                        result += str(self.tile(col,row))
                        result += " "
                    result += "   "
                result += "\n"
            result += "\n"
        return result + "\n\n\n"


    def solve(self):
        '''
        Tries to find solutions for the given sudoku puzzle.
        Returns a list of all solutions found.
        This method must be implemented by derived classes.
        '''
        pass


class RecursiveBoard(BaseBoard):
    '''
    Provides a recursive solving algorithm
    '''

    def __init__(self):
        BaseBoard.__init__(self)


    def __solveInternally(self, col, row):

        def propagate():
            for i in range(col + 1, MAX_COL_INDEX + 1):
                if self._access(i, row) == INTERNAL_FREE:
                    return [i, row]
            for i in range(row + 1, MAX_ROW_INDEX + 1):
                for j in range(9):
                    if self._access(j, i) == INTERNAL_FREE:
                        return [j, i]
            return [MAX_COL_INDEX + 1, MAX_ROW_INDEX + 1]


        def getValidVals():
            vals = [i for i in range(9)]
            # Step one: Remove all values that appear within same column
            for i in range(9):
                tileContent = self._access(col, i)
                if tileContent != INTERNAL_FREE:
                    vals[tileContent] = INTERNAL_FREE
            # Step two: Remove all values that appear within same row
            for i in range(9):
                tileContent = self._access(i, row)
                if tileContent != INTERNAL_FREE:
                    vals[tileContent] = INTERNAL_FREE
            # Step three: Check 'boardlets'
            boardletRow = int(row / 3) * 3
            boardletCol = int(col / 3) * 3
            for c in range(3):
                for r in range(3):
                    tileContent = self._access(boardletCol + c, boardletRow + r)
                    if tileContent != INTERNAL_FREE:
                        vals[tileContent] = INTERNAL_FREE
            return vals


        def printBoard(printStream = sys.stdout):
            printStream.write(str(self))
            printStream.write("\n")


        def printBoardWith(vals, printStream = sys.stdout):
            oldVal = self._access(col, row)
            for val in vals:
                if val != INTERNAL_FREE:
                    self._access(col, row, val)
                    printBoard(printStream)
            self._access(col, row, oldVal)

        if col >= MAX_COL_INDEX and row >= MAX_ROW_INDEX:
            self._solutions.append(self.clone())
            #print  self._solutions
            return
        elif col == 0 and row == 0 and self._access(0, 0) != INTERNAL_FREE:
            [nextCol, nextRow] = propagate()
            self.__solveInternally(nextCol, nextRow)
        else:
            if self._iteration > self._printCycle:
                self._iteration = 0
                printBoard()
            self._iteration += self._iterationRaise
            vals = getValidVals()
            # print [col, row, vals]
            [nextCol, nextRow] = propagate()
            for next in vals:
                if next != INTERNAL_FREE:
                    self._access(col, row, next)
                    self.__solveInternally(nextCol, nextRow)
            self._access(col, row, INTERNAL_FREE)


    def solve(self):
        self.__solveInternally(0, 0)
        return self._solutions



    
class IterativeBoard(BaseBoard):
    '''
    Provides a iterative solving algorithm.
    Should but is not more performant than the recursive one.
    I suspect this is partly due to these neat little traps 'provided' by python.
    I wont optimize further as I am really pissed by these 'features'.
    '''

    def __init__(self):
        BaseBoard.__init__(self)
        self.row = 0
        self.col = 0
        self.solutions = []
        self.metaIteration = 0
        self.iteration = 0
        self.remainingVals = [[OCCUPIED if self._access(j, i) != INTERNAL_FREE 
            else [k for k in range(9)]
            for i in range(9)] for j in range(9)]


    def valsRemaining(self, c, r):
        for i in range(9):
            val = self.remainingVals[c][r][i]
            if val != INTERNAL_FREE  and val != OCCUPIED:
                return True
        return False

        
    def getNextVal(self):
        for i in range(9):
            val = self.remainingVals[self.col][self.row][i]
            if val != INTERNAL_FREE  and val != OCCUPIED:
                self.remainingVals[self.col][self.row][i] = INTERNAL_FREE
                return val
        return False

        
    def propagate(self):
        for i in range(self.col + 1, MAX_COL_INDEX + 1):
            if self._access(i, self.row) == INTERNAL_FREE:
                self.col = i
                return True
        for i in range(self.row + 1, MAX_ROW_INDEX + 1):
            for j in range(9):
                if self._access(j, i) == INTERNAL_FREE:
                    self.col = j
                    self.row = i
                    return True
        return False

            
    def rewind(self):
        i = self.row
        j = self.col
        while i >= 0:
            while j >= 0:
                if not self.remainingVals[j][i] == OCCUPIED:
                    if self.valsRemaining(j, i) :
                        self.row = i
                        self.col = j
                        return True
                    self._access(j, i, INTERNAL_FREE)
                j -= 1
            j  = MAX_COL_INDEX
            i -= 1
        return False


    def setValidVals(self):         
        vals = self.remainingVals[self.col][self.row]
        for i in range(9):
            vals[i] = i
        # Step one: Remove all values that appear within same column
        for i in range(9):
            tileContent = self._access(self.col, i)
            if tileContent != INTERNAL_FREE:
                vals[tileContent] = INTERNAL_FREE
        # Step two: Remove all values that appear within same row
        for i in range(9):
            tileContent = self._access(i, self.row)
            if tileContent != INTERNAL_FREE:
                vals[tileContent] = INTERNAL_FREE
        # Step three: Check 'boardlets'
        boardletRow = int(self.row / 3) * 3
        boardletCol = int(self.col / 3) * 3
        for c in range(3):
            for r in range(3):
                tileContent = self._access(boardletCol + c, boardletRow + r)
                if tileContent != INTERNAL_FREE:
                    vals[tileContent] = INTERNAL_FREE


    def printBoard(self, printStream = sys.stdout):
        printStream.write(str(self))
        printStream.write("\n")


    def solve(self):
        self.row = 0
        self.col = 0
        if not self._access(0, 0) == INTERNAL_FREE:
            if not self.propagate():
                # There are no free fields?
                return
        # Now we should have found a possibly free field
        self.setValidVals()            
        while True:
            if self.iteration >= self._printCycle:
                print(self.metaIteration)
                self.printBoard()
                self.iteration = 0
                self.metaIteration += self._printCycle
            self.iteration += 1
            if not self.valsRemaining(self.col, self.row):
                if not self.rewind():
                    return self._solutions
            self._access(self.col, self.row, self.getNextVal())
            if not self.propagate():
                self.printBoard(sys.stderr)
                print( "Found solution")
                self._solutions.append(self.clone());
                if not self.rewind():
                    return self._solutions
            else:
                self.setValidVals()

            

if __name__ == '__main__':
    # board = IterativeBoard()
    board = RecursiveBoard()
    board.setPrintCycle(1)
    # board.tile(7, 0, 1)
    # board.tile(0, 1, 4)
    # board.tile(1, 2, 2)
    # board.tile(4, 3, 5)
    # board.tile(6, 3, 4)
    # board.tile(8, 3, 7)
    # board.tile(2, 4, 8)
    # board.tile(6, 4, 3)
    # board.tile(2, 5, 1)
    # board.tile(4, 5, 9)
    # board.tile(0, 6, 3)
    # board.tile(3, 6, 4)
    # board.tile(6, 6, 2)
    # board.tile(1, 7, 5)
    # board.tile(3, 7, 1)
    # board.tile(3, 8, 8)
    # board.tile(5, 8, 6)

    #board.tile(0, 0, 2)
    board.tile(0, 1, 9)
    board.tile(0, 3, 7)
    board.tile(0, 4, 5)
    board.tile(0, 7, 1)
    
    board.tile(1, 0, 6)
    board.tile(1, 2, 8)
    board.tile(1, 3, 2)
    board.tile(1, 4, 1)
    board.tile(1, 5, 4)
    board.tile(1, 7, 9)
    board.tile(1, 8, 7)

    board.tile(2, 0, 1)
    board.tile(2, 1, 4)
    board.tile(2, 2, 7)
    board.tile(2, 3, 6)
    board.tile(2, 4, 3)
    board.tile(2, 5, 9)
    board.tile(2, 6, 5)
    board.tile(2, 7, 8)
    board.tile(2, 8, 2)

    board.tile(3, 0, 9)
    board.tile(3, 1, 6)
    board.tile(3, 2, 5)
    board.tile(3, 5, 1)
    board.tile(3, 6, 2)
    board.tile(3, 7, 7)

    board.tile(4, 0, 8)
    board.tile(4, 1, 3)
    board.tile(4, 2, 4)
    board.tile(4, 4, 2)
    board.tile(4, 5, 7)
    board.tile(4, 6, 6)
    board.tile(4, 7, 5)
    board.tile(4, 8, 1)

    board.tile(5, 0, 7)
    board.tile(5, 1, 2)
    board.tile(5, 2, 1)
    board.tile(5, 3, 3)
    board.tile(5, 4, 6)
    board.tile(5, 6, 9)
    board.tile(5, 7, 4)
    board.tile(5, 8, 8)

    board.tile(6, 1, 7)
    board.tile(6, 2, 2)
    board.tile(6, 3, 8)
    board.tile(6, 4, 9)
    board.tile(6, 5, 6)
    board.tile(6, 6, 1)
    board.tile(6, 7, 3)
    board.tile(6, 8, 4)

    board.tile(7, 0, 4)
    board.tile(7, 1, 1)
    board.tile(7, 2, 6)
    board.tile(7, 3, 5)
    board.tile(7, 5, 3)
    board.tile(7, 6, 8)
    board.tile(7, 7, 2)

    board.tile(8, 0, 3)
    board.tile(8, 1, 8)
    board.tile(8, 3, 1)
    board.tile(8, 4, 4)
    board.tile(8, 5, 2)
    board.tile(8, 6, 7)
    board.tile(8, 8, 5)

    print "This is the given board: \n"
    print board
    sys.stderr.write(str(board))
    sys.stderr.write("\n")
    sys.stdin.readline()
    sols = board.solve()
    for i in sols:
        print str(i)

