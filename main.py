# Program to solve the Pentosnake Puzzle
# The Pentosnake puzzle is a puzzle set on an 11x11 grid.
# The initial grid has the positions of the head and tail ends of the snake marked.
# The puzzle also requires there to be a cell marked by F that must be part of a pentomino.

# The following instructions apply:

# Draw a snake (a 1 cell-wide path) in the frid whose head and tail are given by circled cells. The snake can touch itself diagonally, but cannot touch itself orthogonally.

#All cells that are not part of the snake must be part of a pentomino (i.e. an orthogonally connected group of five cells). These unused pentominoes cannot touch orthogonally but can touch diagonally. Pentominoes can be repeated. The F in the grid means that cell must be part of an F pentomino.

import numpy as np

# Define cell states used:
# 2 = snake
# 1 = pentomino
# 0 = blank

def neighbours(row, col):
    # Return coordinates of neighbours
    result = [(row-1,col),(row,col+1),(row+1,col),(row,col-1)]
    # Check if rows and columns are outside grid
    # If outside grid, return -1 for the out-of-bound coordinate
    result = [i if (i[0] >= 0 and i[0] <= 10) else (-1, -1) for i in result]
    result = [i if (i[1] >= 0 and i[1] <= 10) else (-1, -1) for i in result]
    return result

def val_coord(row, col, grid, val):
    # Return the coordinate of neighbours of given cell that matches value
    coords = neighbours(row, col)
    result = [i for i in coords if (grid[i] == val) and i != (-1, -1)]
    return result

def count_neighbours(row, col, grid):
    # Return count of each cell state in neighbours
    coords = neighbours(row, col)
    count = [0, 0, 0]
    for c in coords:
        if c != (-1, -1):
            val = int(grid[c])
            count[val] += 1
    return count

def connected_comp(row, col, grid):
    # Return number of cells in orthogonally connected cluster containing given cell
    val = grid[(row, col)]
    coords = val_coord(row, col, grid, val) + [(row, col)]
    new = coords.copy()
    while len(new)>0:
        temp = []
        for n in new:
            temp += val_coord(n[0], n[1], grid, val)
        new = [t for t in temp if t not in coords]
        coords = coords + new

    unique = list(set(coords))
    return unique

def state_changes(row, col, grid, mode = 0):
    # Update the states of neighbours of the given cell
    # Count the number of neighbours in each state (empty, pentomino, snake)
    count = count_neighbours(row, col, grid)
    # Coordinates of empty cells
    empty_coord = val_coord(row, col, grid, 0)
    # Empty dictionary of changes:
    changes = {}
    if len(empty_coord) == 0:
        # Break if there are no empty cells to update
        return changes
    # Consider cases for different cell value
    val = grid[(row,col)]
    if val == 2:
        # Current cell = 2 case
        if count[2] == 1-mode and count[0] == 1:
            # Continue snake on the only available path
            changes[empty_coord[0]] = 2
        if count[2] == 2-mode:
            # Fill in orthogonally connected cells external to path with pentomino state
            for e in empty_coord:
                changes[e] = 1
    if val == 1:
        # Length of connected pentomino
        connect = connected_comp(row, col, grid)
        # Current cell = 1 case
        if len(connect) == 5:
            # Surround complete pentomino with path
            for e in empty_coord:
                changes[e] = 2
        if len(connect) < 5:
            # Fill in pentomino where there is only one option
            zeros = []
            for c in connect:
                zeros += val_coord(c[0],c[1],grid,0)
            zeros = list(set(zeros))
            if len(zeros) == 1:
                changes[zeros[0]] = 1
    if val == 0:
        # Current cell = 0 case
        pass
    return changes

def pentomino_check(row, col, grid):
    # Return validity(bool) of pentomino
    # 1 - pentomino still valid
    # 0 - invalid pentomino
    connect = connected_comp(row, col, grid)
    if len(connect) == 5:
        return 1
    elif len(connect) < 5:
        for c in connect:
            empty_coord = val_coord(c[0], c[1], grid, 0)
            if len(empty_coord) > 0:
                return 1
    return 0

def complete_check(grid):
    # Return validaty(bool) of snake path
    # 1 - snake valid
    # 0 - snake connects head to tail without completing grid
    connect = connected_comp(tail[0], tail[1], grid)
    if head in connect:
        return not np.any(grid == 0)
    else:
        return 1


# Define max number of steps
max_steps = 50

# Define head and tail coordinates
head = (8, 7)
tail = (10, 8)

# Initialise grid
grid = np.zeros((11,11))
print('Initialising grid...')
# Mark positions of head and tail
grid[head] = 2
grid[tail] = 2

# Mark position of the first F-pentomino
grid[9][7:10] = 1
grid[10][7] = 1
grid[8][8] = 1
print(grid)

# Initialise the loop
next_grid = grid.copy()

for i in range(11):
    for j in range(11):
        if grid[(i, j)] != 0:
            if (i, j) == head or (i, j) == tail:
                changes = state_changes(i, j, grid, 1)
                for e in changes:
                    next_grid[e] = changes[e]
            else:
                changes = state_changes(i, j, grid, 0)
                print('Current' + str(i) + str(j))
                print(changes)
                for e in changes:
                    print('Change val')
                    print(changes[e])
                    next_grid[e] = changes[e]
print('Step = 1')
print(next_grid)

counter = 0

while not np.array_equal(next_grid, grid) and (counter < max_steps - 1):
    # While grid is still changing, keep updating grid
    # Save the current state of the grid to use as reference before updating
    grid = next_grid.copy()
    for i in range(11):
        for j in range(11):
            if grid[(i, j)] != 0:
                if (i, j) == head or (i, j) == tail:
                    changes = state_changes(i, j, grid, 1)
                    for e in changes:
                        next_grid[e] = changes[e]
                else:
                    changes = state_changes(i, j, grid, 0)
                    for e in changes:
                        next_grid[e] = changes[e]
    print('Step = ' + str(counter + 2))
    print(next_grid)
    counter += 1