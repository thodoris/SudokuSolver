# Solve Sudoku Diagonal Problems

## Synopsis

This project implements a Sudoku-solving agent able to solve diagonal Sudoku puzzles.
A diagonal Sudoku puzzle is identical to traditional Sudoku puzzles with the added constraint that the boxes on the two main diagonals of the board must also contain the digits 1-9 in each cell (just like the rows, columns, and 3x3 blocks).

## Motivation

The idea for this project has been based on  Peter Norvig's excellent post : Solving Every Sudoku Puzzle (http://norvig.com/sudoku.html).
Some extra strategies have been implemented (such as the naked twins strategy) in order to be able to solve harder problems.


## Run the code 

    `$ python sudoku.py [--puzzle PUZZLE_STRING]`
	
	Parameters
    ----------
    puzzle(string)
        a string representing a sudoku grid. Empty cells denoted using a dot
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

## Run the local test suite

    `$ python -m unittest -v`



