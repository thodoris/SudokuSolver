rows = 'ABCDEFGHI'
cols = '123456789'
boxes = [r + c for r in rows for c in cols]


def cross(A, B):
    """Cross product of elements in A and elements in B """
    return [x+y for x in A for y in B]


def values2grid(values):
    """Convert the dictionary board representation to as string

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    """
    res = []
    for r in rows:
        for c in cols:
            v = values[r + c]
            res.append(v if len(v) == 1 else '.')
    return ''.join(res)


def grid2values(grid):
    """Convert grid into a dict of {square: char} with '123456789' for empties.

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    Returns
    -------
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
            then the value will be '123456789'.
    """
    sudoku_grid = {}
    for val, key in zip(grid, boxes):
        if val == '.':
            sudoku_grid[key] = '123456789'
        else:
            sudoku_grid[key] = val
    return sudoku_grid


def display(values):
    """Display the values as a 2-D grid.

    Parameters
    ----------
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print()


