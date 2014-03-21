import pprint
import sys

import ipdb
from termcolor import colored

grid_pic = """
|||||||||
|S|     |
| | | |||
|       |
| ||||| |
|       |
| |||||||
|      E|
|||||||||
"""

sp = (1,1)
ep = (8,8)

# Construct grid from ascii pic
def grid_from_pic(pic):
    '''
    returns a 2D matrix (grid representation) from a multiline ascii string
    '''

    grid = [[cell for cell in row] for row in pic.split('\n')][1:-1]
    return grid

def print_grid(grid):
    '''
    prints a pretty representation of the grid to stdout
    '''

    for row in grid:
        print(''.join(row))

def print_path(grid, path):
    '''
    prints a pretty representation of a given path overlaid on a grid to
    stdout
    '''

    for cell in path:
        if cell:
            grid[cell[1]][cell[0]] = colored('.', 'red')

    print()
    print_grid(grid)
    print()


def is_open(cell):
    '''
    returns True is cell is not a wall
    '''

    return cell is not '|'

def find_open_cells(grid, cells):
    '''
    returns a list of cells that are not walls
    '''

    return [ c for c in cells if is_open(grid[c[1]][c[0]]) ]

def find_point_from_char(grid, char):
    for y, row in enumerate(grid):
        try:
            x = row.index(char)
            sp = x, y
        except ValueError:
            pass
    return sp

def cell_from_offset(grid, cell, offset):
    '''
    takes a cell as (x, y) tuple and an offset as (x, y) tuple and returns
    the translated (x, y) tuple if it exists
    '''

    x = cell[0] + offset[0] 
    y = cell[1] + offset[1] 

    if x < 0 or y < 0:
        raise IndexError("Cell (%s, %s) outside of grid bounds." % (x, y))

    return (x, y)

def cells_surrounding(grid, cell):
    '''
    returns a list of (x, y) tuples for each cell adjacent up, down, left, and
    right
    '''

    directions = [
        (0, -1), #up
        (0,  1), #down
        (-1, 0), #left
        (1,  0), #right
    ]
    cells = []

    for d in directions:
        try:
            c = cell_from_offset(grid, cell, d)
            cells.append(c)
        except IndexError:
            pass

    return cells

def path_from_point(grid, endpoint, path):
    paths = []

    last = path[-1]

    #print('last', last)
    #print('endpoint', endpoint)
    if last == endpoint:
        #print('\nyay\n')
        #print(path)
        return path

    surrounding = cells_surrounding(grid, last)
    open_cells = find_open_cells(grid, surrounding)

    if not open_cells:
        raise Exception("No open cells.")

    for o in open_cells:
        if not o in path:  # prevent intersections
            p = path_from_point( grid, endpoint, path + [o] )
            if p:
                paths.append(p)

    if len(paths) == 1:
        return paths[0]

    return paths


def run():
    '''
    main loop.
    consumes an ASCII grid representation and creates a 2D matrix.
    finds the start (sp) and end (ep) points and finds shortest path.
    '''

    grid = grid_from_pic(grid_pic)
    print_grid(grid)

    sp = find_point_from_char(grid, 'S')
    ep = find_point_from_char(grid, 'E')
    print()
    print('starting point:', sp)
    print('ending point:',   ep)
    print()

    paths = path_from_point(grid, ep, [sp])

    if not paths:
        raise Exception("No path could be found.")

    if type(paths[0]) is not list:
        paths = [paths]

    print()
    print('Found %s paths.' % len(paths))
    print(paths)
    for i, path in enumerate(paths):
        n = i + 1
        print()
        print('Path %s' % n)
        print('\tLength: %s' % len(path))
        print('\t', path)

        print_path(grid, path)


if __name__ == "__main__":
    run()
