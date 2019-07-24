#!/usr/bin/python3
#------------------------------------------------------------------------------
#
# (C) 2019 Michael J. Beer
#
# All rights reserved.
#
# Redistribution  and use in source and binary forms, with or with‐
# out modification, are permitted provided that the following  con‐
# ditions are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above  copy‐
# right  notice,  this  list  of  conditions and the following dis‐
# claimer in the documentation and/or other materials provided with
# the distribution.
#
# 3.  Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote  products  derived
# from this software without specific prior written permission.
#
# THIS  SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBU‐
# TORS "AS IS" AND ANY EXPRESS OR  IMPLIED  WARRANTIES,  INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE  ARE  DISCLAIMED.  IN  NO  EVENT
# SHALL  THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DI‐
# RECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR  CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS IN‐
# TERRUPTION)  HOWEVER  CAUSED  AND  ON  ANY  THEORY  OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING  NEGLI‐
# GENCE  OR  OTHERWISE)  ARISING  IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#------------------------------------------------------------------------------

"""
General-purpose Signalling Server for testing.

@author Michael J. Beer, DLR/GSOC
@copyright 2019 Michael J. Beer, michael.josef.beer@googlemail.com
@date 2019-04-19

@license BSD 3-Clause
@version 1.0.0

@status Development

"""

#------------------------------------------------------------------------------

import sys

#-------------------------------------------------------------------------------

class Square:

    def __init__(self):
        self._possibilities = [i for i in range(1, 10)]
        self._listeners = []

    def copy(self):
        new_square = Square()
        new_square._possibilities = self._possibilities.copy()
        new_square._listeners = self._listeners.copy()
        return new_square

    def __str_matrix(self):
        content = []
        row = []
        for i in range(1, 10):
            v = i
            if v not in self._possibilities:
                v = ' '
            row.append(str(v))
            if i % 3 == 0:
                content.append("".join(row))
                row = []
        return '\n'.join(content)

    def __str__(self):
        if self.is_pinned():
            return str(self.pinned_value())
        return self.__str_matrix()

    def _notify_all(self):
        for listener in self._listeners:
            listener(self)

    def possibilities(self, new_possibilities=None):
        current = self._possibilities
        if new_possibilities:
            self._possibilities = new_possibilities
        return current

    def set(self, v):
        p = self._possibilities
        if not v in p:
            return None
        self._possibilities = [v]
        self._notify_all()
        return p

    def pinned_value(self):
        if self.is_pinned():
            return self._possibilities[0]
        return None

    def is_pinned(self):
        return len(self._possibilities) == 1

    def drop(self, x):
        """
        Returns True if value could be removed.
        Returns False if the value could not be removed from possibilities
        (because it was not contained within)
        """

        if x in self._possibilities:
            self._possibilities.remove(x)
            self._notify_all()
            return True
        return False

    def change_listener(self, listener):
        self._listeners = [listener]

#-------------------------------------------------------------------------------

class Field:

    def __init__(self):
        self._squares = [[Square() for i in range(1,10)] for i in range(1,10)]

    #---------------------------------------------------------------------------

    def set(self, x, y, value):
        if not (1 <= x <= 9):
            return False

        if not (1 <= y <= 9):
            return False

        if not (1 <= value <= 9):
            return False

        if not self._squares[y - 1][x - 1].set(value):
            return False

        self._pin(x, y, value)

    #---------------------------------------------------------------------------

    def copy(self):
        new_field = Field()
        new_squares = []
        for row in self._squares:
            new_row = []
            new_squares.append(new_row)
            for square in row:
                new_row.append(square.copy())

        new_field._squares = new_squares

        return new_field

    #---------------------------------------------------------------------------

    def get_square(self, x, y):

        return self._squares[y - 1][x - 1]

    #---------------------------------------------------------------------------

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

    #---------------------------------------------------------------------------

    def _remove_from_row(self, x, y, value):
        """
        Returns a list of all coords that could be pinned down to
        one certain value during this remove action
        """

        pinned = []
        for yv in range(1, 10):
            if not yv == y:
               s = self._squares[yv - 1][x - 1]
               if s.drop(value) and s.is_pinned():
                   pinned.append((x, yv, s.pinned_value()))
        return pinned

    #---------------------------------------------------------------------------

    def _remove_from_column(self, x, y, value):
        pinned = []
        for xv in range(1, 10):
            if not xv == x:
               s = self._squares[y - 1][xv - 1]
               if s.drop(value) and s.is_pinned():
                   pinned.append((xv, y, s.pinned_value()))
        return pinned

    #---------------------------------------------------------------------------

    def _remove_from_subfield(self, x, y, value):
        pinned = []
        x_subfield = int((x - 1) / 3)
        y_subfield = int((y - 1) / 3)
        for xv in [x_subfield * 3 + i for i in range(1, 4)]:
            for yv in [y_subfield * 3 + i for i in range(1, 4)]:
                if xv == x and yv == y:
                    continue
                s = self._squares[yv - 1][xv - 1]
                if s.drop(value) and s.is_pinned():
                    pinned.append((xv, yv, s.pinned_value()))
        return pinned

    #---------------------------------------------------------------------------

    def __str__(self):

        rows = []
        lineno = 1
        for y in self._squares:
            row = []
            colno = 1
            for x in y:
                row.append(
                        "[" +
                        " ".join( [str(v) for v in x.possibilities()]) +
                        "]" + str("   "))
                colno = (colno + 1) % 3
                if colno == 1:
                    row.append("  ")
            rows.append(" ".join(row))
            lineno = (lineno + 1) % 3
            if lineno == 1:
                rows.append("")
        return "\n".join(rows)

    #---------------------------------------------------------------------------

    def print(self):
        sys.stdout.write(str(self))

    #---------------------------------------------------------------------------

    def __next_solution(self, anounce_solution, col, row):
        """Needs rework!!!!"""

        def next_coordinates(x, y):
            if y < 9:
                return (x, y + 1)
            if x < 9:
                return (x + 1, 1)
            return None

        possibilities = self.get_square(col, row).possibilities().copy()

        if 1 > len(possibilities):
            return False

        next_coord = next_coordinates(col, row)

        if not next_coord:
            for p in possibilities:
                print("Last {}:{} : {} ({})".format(col, row, p, possibilities))
                solve_board = self.copy()
                solve_board.set(col, row, p)
                anounce_solution(self)
            return 0 < len(possibilities)

        next_col, next_row = next_coord

        solution_found = False

        for p in possibilities:
            solve_board = self.copy()
            solve_board.set(col, row, p)
            print("Next {}:{} : {} ({})".format(next_col, next_row, p, possibilities))
            solution_found = solve_board.__next_solution(anounce_solution, next_col, next_row) or solution_found

        return solution_found

    #---------------------------------------------------------------------------

    def next_solution(self, anounce_solution=None):

        if not anounce_solution:
            anounce_solution=lambda x: sys.stdout.write(str(x))
        solution_found = self.__next_solution(anounce_solution, 1, 1)
        return solution_found

