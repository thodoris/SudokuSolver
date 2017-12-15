import argparse
from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#Calculate diagonial Units
diag1_units=[x+y for x,y in zip(rows, cols)]
diag2_units=[x+y for x,y in zip(rows, cols[::-1])]
diag_units=[diag1_units]+[diag2_units]

unitlist = row_units + column_units + square_units + diag_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    for u in unitlist:
        doubles_in_unit = [values[box] for box in u if len(values[box])==2] #all box values in the unit with length 2 (e.g. 37 , 45 , 67)
        twins_in_unit = set([x for x in doubles_in_unit if doubles_in_unit.count(x) > 1]) #only those that apperas at least twice in the unit
        target_boxes = [box for box in u if (len(values[box])>1 and values[box] not in twins_in_unit ) ] #search domain (all the boxes in the unit with values of length greater than 2)
        for dd in twins_in_unit: #itterate twins
            for t in target_boxes: #eliminate twin digits from target_boxes
                values[t]=values[t].replace(dd[0],'')
                values[t]=values[t].replace(dd[1],'')
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for u in unitlist:
       for digit in cols:
            dplaces = [box for box in u if digit in values[box]]
            if len(dplaces) == 1: # d can be only in one place
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values=eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values=only_choice(values)
        # Use the Naked Twins Strategy
        values=naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values or if there are duplicate values inside the same unit 
        if len([box for box in values.keys() if len(values[box]) == 0]) or not check_constraint(values):
            return False
    return values

def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    values=reduce_puzzle(values)
    if values is False:
        return False ## Failed to reduce
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    length,key = min( (len(values[box]),box) for box in values.keys() if len(values[box]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for test_value in values[key]:
        new_board = values.copy()
        new_board[key] = test_value
        is_solved = search(new_board)
        if is_solved: #is true
            return is_solved

def check_constraint(values):
    """Checks in the dictionary representation of the solution for duplicate values inside the same unit

    Parameters
    ----------
   values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
        
    Returns
    -------
    True or False
        False if there are duplicate values inside the same unit , otherwise True
    """
    for unit in unitlist:
        filled_boxes = [box for box in unit if len(values[box]) == 1]
        unitValues = ''.join([values[box] for box in filled_boxes])
        duplicate_digit = [digit for digit in '123456789' if unitValues.count(digit) > 1]
        if duplicate_digit:
            return False
    return True

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    #default puzzle
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # initiate the parser
    parser = argparse.ArgumentParser()
    # add puzzle argument
    parser.add_argument("--puzzle", "-p", help="set the puzzle as a string")
    # read arguments from the command line
    args = parser.parse_args()

    # check for --puzzle
    if args.puzzle:  
        diag_sudoku_grid=args.puzzle
        print("puzzle set by user :  %s" % diag_sudoku_grid)
    else:
        print("using default puzzle :  %s" % diag_sudoku_grid)    
    print("-------------------------------------------------------------------------------------------------------")
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

   