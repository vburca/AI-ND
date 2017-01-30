from utils import *

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    # Check for previous errors
    if values is False:
        return False

    # Check if we are done
    if all(len(values[box]) == 1 for box in boxes):
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    _, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[box]:
        new_values = values.copy()
        new_values[box] = value
        attempt = search(new_values)
        if attempt:
            return attempt