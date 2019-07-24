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

from tkinter import *
from tkinter.ttk import Separator
from sudoku  import Field

from enum import Enum

import sys

#-------------------------------------------------------------------------------

class SquareSelector:

    def __init__(self, parent, field, x, y):


        frame = Toplevel(parent)

        def close_us(event):
            frame.destroy()

        def create_selection_setter_and_closer(value):
            def set_and_close():
                field.set(x, y, value)
                frame.destroy()
            return set_and_close

        frame.bind("<FocusOut>", close_us)
        frame.grab_set()

        possibilities = field.get_square(x, y).possibilities()

        for r in range(3):
            frame.grid_columnconfigure(r, weight=0)
            for c in range(3):
                frame.grid_rowconfigure(c, weight=0)
                value = 1 + c + r * 3
                if value in possibilities:
                    button = Button(frame, text=str(value), command=create_selection_setter_and_closer(value))
                else:
                    button = Button(frame, text=str(' '), state=DISABLED)
                button.grid(row=r, column=c)

#-------------------------------------------------------------------------------

class SquareWidget:

    def __init__(self, parent, field, x, y):

        def show_selector():
            SquareSelector(parent, field, x, y)

        self.__field = field
        self.__square = field.get_square(x, y)
        self.__coords = (x, y)
        self.__widget = Button(parent)
        self.__textvar = StringVar()

        self.__widget.config(width=3, height=3, textvariable=self.__textvar, command=show_selector)
        self.__square.change_listener(lambda x: self.update())
        self.update()

    def update(self):
        self.__textvar.set(str(self.__square))

    def __getattr__(self, name):
        return getattr(self.__widget, name)

#-------------------------------------------------------------------------------

class GuiMode(Enum):

    SOLVE = "solve"
    SHOW = "show"

def create_gui(root, field=Field(), mode=GuiMode.SOLVE):

    def show_solution(field):
        print(str(field))
        create_gui(root, field=field, mode=GuiMode.SHOW)



    def solve_field():
        field.next_solution(show_solution)

    for c in range(3):
        root.grid_columnconfigure(c, weight=0)

    for r in range(3):
        root.grid_rowconfigure(r, weight=0)

    current_col = 0
    current_row = 0

    for r in range(9):
        for c in range(9):
            w = SquareWidget(root, field, r + 1, c + 1)
            w.grid(column=current_col, row=current_row)
            current_col += 1
            if (c + 1) % 3 == 0:
                w = Separator(root, orient="vertical")
                w.grid(column=current_col, row=current_row)
                current_col += 1

        current_col = 0
        current_row += 1

        if (r + 1) % 3 == 0:
            w = Separator(root, orient="horizontal")
            w.grid(column=current_col, row=current_row)
            current_row += 1

    frame = Frame(root)
    frame.grid_columnconfigure(0, weight=0)
    frame.grid(columnspan=9 + 2, row=current_row, sticky="NESW")

    button_command = solve_field
    button_text = "Solve"

    var = IntVar()

    if GuiMode.SHOW == mode:
        button_command = lambda: var.set(1)
        button_text = "Next solution"

    button = Button(frame, text=button_text, command=button_command)
    button.grid()

    if GuiMode.SHOW == mode:
        button.wait_variable(var)
        frame.destroy()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main = create_gui(Tk())
    mainloop()

