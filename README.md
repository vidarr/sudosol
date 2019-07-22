# sudosol

Sudoku solver with a simple GUI

# Setup

There is no setup.

# Execution

Just call

    python gui.py

This will give you a blank sudoku board where you can place preset numbers.
Click 'Solve' at the bottom and wait...
As soon as all solutions have been found (if you use a Sudoku posed within a
magazine or so there should only be ONE ) the board will be filled with the 
first solution and the 'Solve' button will turn into a 'Next solution' button.
Clicking it will present you another solution if one is available.

That's it.

# Beware

Currently, the solver has been redesigned to filter out impossible solutions
as soon as a value of a field has been pinned down to one value.

This should suffice to solve a sudoku with a unique solution.

If there are several solutions, however, the current version has not been provided
with the iterative solver yet.

The old version with the iterative solver is still available underneath the tag
'1.0' .


