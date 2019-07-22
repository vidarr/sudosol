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

def next_coordinates(x, y):
    if y < 3:
        return (x, y + 1)
    if x < 3:
        return (x + 1, 1)
    return None

#-------------------------------------------------------------------------------

class Square:

    def __init__(self):
        self._possibilities = [i for i in range(1, 10)]
        self._listeners = []

    def __str__(self):
        content = []
        row = []
        for i in range(1, 10):
            v = i
            if v not in self._possibilities:
                v = ' '
            row.append(str(v))
            print("{}: {}".format(i, row))
            if i % 3 == 0:
                content.append("".join(row))
                row = []
        return '\n'.join(content)

    def _notify_all(self):
        for listener in self._listeners:
            listener(self)

    def possibilities(self):
        return self._possibilities

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

        if len(self._possibilities) < 1:
            raise("Cannot drop")
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
        # During solution process, this 'shadow field' will keep a list of
        # values not tried yet.
        self._solution_state = [[[] for i in range(1,10)] for i in range(1,10)]
        self._solution_current_field = [1,1]

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

        self._pin(x, y, v)

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
        print("Going to drop " + str(x) + ":" + str(y))
        pinned = []
        x_subfield = int((x - 1) / 3)
        y_subfield = int((y - 1) / 3)
        for xv in [x_subfield * 3 + i for i in range(1, 4)]:
            for yv in [y_subfield * 3 + i for i in range(1, 4)]:
                if xv == x and yv == y:
                    continue
                print("Dropping " + str(value) + " from " +
                        str(yv) + ":" + str(xv))
                s = self._squares[yv - 1][xv - 1]
                if s.drop(value) and s.is_pinned():
                    pinned.append((xv, yv, s.pinned_value()))
        return pinned

    #---------------------------------------------------------------------------

    def print(self):

        lineno = 1
        for y in self._squares:
            colno = 1
            for x in y:
                sys.stdout.write(
                        "[" +
                        " ".join( [str(v) for v in x.possibilities()]) +
                        "]" + str("   "))
                colno = (colno + 1) % 3
                if colno == 1:
                    sys.stdout.write("  ")
            sys.stdout.write("\n")
            lineno = (lineno + 1) % 3
            if lineno == 1:
                sys.stdout.write("\n")

    #---------------------------------------------------------------------------

    def next_solution(self):
        # Continue with state in solution_state and solution_current_field
        pass

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    # field = Field()
    # line = " "
    # while line:
    #     line = sys.stdin.readline()
    #     line = line.strip()
    #     if len(line) != 3:
    #         continue
    #     x = int(line[0])
    #     y = int(line[1])
    #     v = int(line[2])
    #     field.set(x, y, v)
    #     field.print()

    coords = (1, 1)

    while coords:
        x, y = coords
        print("Coords are " + str(x) + "|" + str(y))
        coords = next_coordinates(x, y)

    
