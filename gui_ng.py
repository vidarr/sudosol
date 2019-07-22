from   tkinter import *
from   sudoku_ng  import Square

import sys

#-------------------------------------------------------------------------------

class SquareSelector:

    def __init__(self, parent, square):


        frame = Toplevel(parent)

        def close_us(event):
            frame.destroy()

        def create_selection_setter_and_closer(value):
            def set_and_close():
                square.set(value)
                frame.destroy()
            return set_and_close

        frame.bind("<FocusOut>", close_us)
        frame.grab_set()
        for y in range(3):
            frame.grid_columnconfigure(y, weight=0)
            for x in range(3):
                frame.grid_rowconfigure(x, weight=0)
                value = 1 + x + y * 3
                button = Button(frame, text=str(value), command=create_selection_setter_and_closer(value))
                button.grid(row=y, column=x)

#-------------------------------------------------------------------------------

class SquareWidget:

    def __init__(self, parent, square):

        def show_selector():
            SquareSelector(parent, square).get_selection()

        self.__square = square
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

    square = Square()

    for c in [0]:
        root.grid_columnconfigure(c, weight=0)

    for r in [0]:
        root.grid_rowconfigure(r, weight=0)

    square_widget = SquareWidget(root, square)
    square_widget.grid(column=0, row=0)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    # board = RecursiveBoard()

    main = create_gui(Tk())
    mainloop()

