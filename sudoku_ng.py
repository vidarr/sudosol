import sys

class Square:

    def __init__(self):
        self._possibilities = [i for i in range(1, 10)]

    def possibilities(self):
        return self._possibilities

    def set(self, v):
        p = self._possibilities
        if not v in p:
            return None
        self._possibilities = [v]
        return p

    def pinned_value(self):
        if self.is_pinned():
            return self._possibilities[0]
        return None
    
    def is_pinned(self):
        return len(self._possibilities) == 1
    
    def drop(self, x):
        """Returns True if value could be removed. Returns False if the value could not be removed from possibilities (because it was not contained within)"""
        if len(self._possibilities) < 1:
            raise("Cannot drop")
        if x in self._possibilities:
            self._possibilities.remove(x)
            return True
        return False

class Field:

    def __init__(self):
        self._squares = [[Square() for i in range(1,10)] for i in range(1,10)]

    def set(self, x, y, value):
        if not (1 <= x <= 9):
            return False

        if not (1 <= y <= 9):
            return False

        if not (1 <= value <= 9):
            return False

        if not self._squares[y - 1][x - 1].set(value):
            return False
        
        self._pin(x, y, v)

    def _pin(self, x, y, v):
        new_pinned = [(x,y,v)]

        while new_pinned:
            pinned = new_pinned
            new_pinned = []
            for x,y,v in pinned:        
                new_pinned = new_pinned + self._remove_from_row(x, y, v)
                new_pinned = new_pinned + self._remove_from_column(x, y, v)
                new_pinned = new_pinned + self._remove_from_subfield(x, y, v)

        return True
    
    def _remove_from_row(self, x, y, value):
        """Returns a list of all coords that could be pinned down to one certain value during this remove action"""
        pinned = []
        for yv in range(1, 10):
            if not yv == y:
               s = self._squares[yv - 1][x - 1]
               if s.drop(value) and s.is_pinned():
                   pinned.append((x, yv, s.pinned_value()))
        return pinned
                   
                   

    def _remove_from_column(self, x, y, value):
        pinned = []
        for xv in range(1, 10):
            if not xv == x:
               s = self._squares[y - 1][xv - 1]
               if s.drop(value) and s.is_pinned():
                   pinned.append((xv, y, s.pinned_value()))
        return pinned

    def _remove_from_subfield(self, x, y, value):
        print("Going to drop " + str(x) + ":" + str(y))
        pinned = []
        x_subfield = int((x - 1) / 3)
        y_subfield = int((y - 1) / 3)
        for xv in [x_subfield * 3 + i for i in range(1, 4)]:
            for yv in [y_subfield * 3 + i for i in range(1, 4)]:
                if xv == x and yv == y:
                    continue
                print("Dropping " + str(value) + " from " + str(yv) + ":" + str(xv))
                s = self._squares[yv - 1][xv - 1]
                if s.drop(value) and s.is_pinned():
                    pinned.append((xv, yv, s.pinned_value()))
        return pinned                
    
    def print(self):

        lineno = 1
        for y in self._squares:
            colno = 1
            for x in y:
                sys.stdout.write("[" + " ".join([str(v) for v in x.possibilities()]) + "]" + str("   "))
                colno = (colno + 1) % 3
                if colno == 1:
                    sys.stdout.write("  ")
            sys.stdout.write("\n")
            lineno = (lineno + 1) % 3
            if lineno == 1:
                sys.stdout.write("\n")

if __name__ == "__main__":
    field = Field()
    line = " "
    while line:
        line = sys.stdin.readline()
        line = line.strip()
        if len(line) != 3:
            continue
        x = int(line[0])
        y = int(line[1])
        v = int(line[2])
        field.set(x, y, v)
        field.print()

