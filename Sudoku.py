
# coding: utf-8

# ### Util Functions

# In[2]:

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


# In[4]:

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]


# In[5]:

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    return dict(zip(boxes, map(lambda x: '123456789' if x == '.' else x, grid)))


# In[6]:

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


# ### Eliminate strategy

# In[7]:

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box in values.keys(): 
        if len(values[box]) == 1:
            for peer in peers[box]:
                assign_value(values, peer, values[peer].replace(values[box], ''))
                # values[peer] = values[peer].replace(values[box], '')
    return values


# ### Only Choice strategy

# In[8]:

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            d_places = [box for box in unit if digit in values[box]]
            if len(d_places) == 1:
                assign_value(values, d_places[0], digit)
                # values[d_places[0]] = digit    
    return values


# ### [Naked Twins](http://www.sudokudragon.com/sudokustrategy.htm#XL2104) strategy

# In[3]:

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        valuelist = [(values[box], box) for box in unit if len(values[box]) == 2]
        valuelist = sorted(valuelist)
        for i in range(len(valuelist) - 1):
            _, box = valuelist[i]
            _, next_box = valuelist[i+1]
            if values[box] == values[next_box]:
                for _box in unit:
                    if _box != box and _box != next_box:
                        assign_value(values, _box, values[_box]
                            .replace(values[box][0], '')
                            .replace(values[box][1], ''))
                i += 2
    return values


# ### Reduce algorithm

# In[9]:

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


# ### Search algorithm

# In[10]:

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    
    if all(len(values[box]) == 1 for box in boxes):
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    _, next_box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[next_box]:
        new_sudoku = values.copy()
        assign_value(new_sudoku, next_box, value)
        # new_sudoku[next_box] = value
        attempt = search(new_sudoku)
        if attempt: 
            return attempt
    
    return False


# ### Sudoku solver

# In[11]:

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


# ### Example

# In[12]:

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[s + t for s, t in zip(rows, cols)]] + [[s + t for s, t in zip(rows, cols[::-1])]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


# In[1]:

assignments = []


# In[13]:

diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
display(solve(diag_sudoku_grid))

try:
    from visualize import visualize_assignments
    visualize_assignments(assignments)

except SystemExit:
    pass
except:
    print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')


# In[ ]:



