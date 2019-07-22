from   tkinter import *
from   sudoku_ng  import Square

import sys

#-------------------------------------------------------------------------------

class SquareSelector:

    def __init__(self, parent, square):
        pass

    def get_selection(self):
        return 6

#-------------------------------------------------------------------------------

class SquareWidget:

    def __init__(self, parent, square):

        def show_selector():
            selection = SquareSelector(parent, square).get_selection()
            if selection:
                self.__square.set(selection)

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

