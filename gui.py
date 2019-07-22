from tkinter import *
from tkinter.ttk import Separator
from sudoku  import Field

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
        print(str(self.__square))

    def __getattr__(self, name):
        return getattr(self.__widget, name)

#-------------------------------------------------------------------------------

def create_gui(root):

    field = Field()

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

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    # board = RecursiveBoard()

    main = create_gui(Tk())
    mainloop()

