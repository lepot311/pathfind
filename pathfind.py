import json
import pprint
import sys

from termcolor import colored

small_maze = """
|||||||||
|S      |
| ||| |||
|       |
| || || |
|       |
| || ||||
|      E|
|||||||||
"""

large_maze = """
|||||||||||||||||||||||||
|S     ||     ||||||    |
| ||||    ||| |||||  || |
|    | ||||||       ||| |
| || |   |||| |||  || | |
|||| |||      ||||    | |
||   |||| || ||| |||||| |
|| |      || | |        |
|| || |||||| | | ||| ||||
|  || |||||| | | |      |
|| || ||     | | | ||||||
|| || || ||||| | |     ||
|| ||    ||    | | ||| ||
|| |||| ||| |||| |   | ||
||   |           ||| | ||
|| | | ||||||||||| | | ||
|  | | ||      |   | | ||
| |||| || |||| | | | ||||
| |   ||    || | ||| ||||
| | |||||||||  | ||  ||||
| | ||        || ||     |
| |    ||||||||| |||||| |
| ||||||||||      ||||| |
|            ||||      E|
|||||||||||||||||||||||||
"""

class Maze(object):
    type_map = {
        ' ': 'space',
        '|': 'wall',
        'S': 'start',
        'E': 'end',
    }

    def __init__(self, grid=None):
        self.solutions = []

        if not grid:
            grid = self.grid_from_pic()

        self.grid = [[ Cell(self, x, y, char) \
                for x, char in enumerate(row) ]
                    for y, row in enumerate(grid) ]

        for row in self.grid:
            for cell in row:
                if cell.char is 'S':
                    self.starting_point = cell
                #elif cell.char is 'E':
                    #self.ending_point = cell

    @property
    def flattened(self):
        return [ cell for row in self.grid for cell in row]

    @property
    def walls(self):
        return [ cell for cell in self.flattened if cell.is_wall ]

    @property
    def height(self):
        return len(self.grid)

    @property
    def width(self):
        return len(self.grid[0])

    @property
    def grid_as_json(self):
        ## TODO: perchance herein lies the problem
        grid = [[ { 'type': Maze.type_map[cell.char] }
                   for cell in row ]
                       for row in self.grid ]
        print(grid)
        return grid

    def grid_from_json(self, json_grid):
        type_map = {
            'space': ' ',
            'wall':  '|',
            'start': 'S',
            'end':   'E',
        }
        self.grid = [[ Cell(self, x, y, type_map[cell['type']])
                      for y, cell in enumerate(row) ]
                          for x, row in enumerate(json_grid) ]

    @property
    def solutions_as_json(self):
        solutions = []

        #print(self.solutions[0])
        #print()
        #print()

        for s in self.solutions:
            grid = self.grid_as_json
            for cell in s:
                grid[cell.y][cell.x]['type'] = 'path'
            solutions.append(grid)

        #result = solutions[0]
        #for row in result:
            #print(row)

        return solutions


    @property
    def as_dict(self):
        response = { 
            'grid': self.grid_as_json,
        }
        if self.solutions:
            response['solutions'] = self.solutions_as_json
        return response

    def grid_from_pic(self, pic=small_maze):
        '''
        returns a 2D matrix (grid representation) from a multiline ascii string

        strips the first and last lines for better ascii art representation
        '''
        return [[cell for cell in row] for row in pic.split('\n')][1:-1]

    def print_grid(self, path=None):
        '''
        prints a pretty representation of the grid to stdout
        '''
        for row in self.grid:
            print()
            for cell in row:
                if path and cell in path:
                    print(colored('.', 'red'), end='')
                    continue
                cell.print_char()
        print()

    def cell_at(self, x, y):
        return self.grid[y][x]

    def solve(self):
        self.starting_point.pathfind([])


class Cell(object):
    colors = {
        'S': 'green',
        'E': 'red',
    }

    directions = [
        ( 0, -1), #up
        ( 0,  1), #down
        (-1,  0), #left
        ( 1,  0), #right
    ]

    def __init__(self, maze, x, y, char=''):
        self.maze = maze
        self.x = x
        self.y = y
        self.char = char
        self.is_wall = self.char is '|'

    def __repr__(self):
        return "Cell (%s, %s)" % (self.x, self.y)

    def print_char(self):
        try:
            print(colored(self.char, Cell.colors[self.char]), end='')
        except KeyError:
            print(colored(self.char, 'white'), end='')

    def pathfind(self, path):
        branches = [ n for n in self.neighbors \
                        if not n.is_wall \
                        and not n in path ]

        for b in branches:
            if b.is_ending_point:
                self.maze.solutions.append(path + [self])
            else:
                b.pathfind(path + [self])

    @property
    def coords(self):
        return (self.x, self.y)

    @property
    def is_ending_point(self):
        return ( self.char is 'E' )

    @property
    def neighbors(self):
        '''
        returns a list of (x, y) tuples for each cell adjacent up, down, left, and
        right
        '''
        cells = []
        for direction in Cell.directions:
            x = self.x + direction[0]
            y = self.y + direction[1]

            try:
                cells.append(self.maze.cell_at(x, y))
            except IndexError:
                pass
        return cells


def run():
    '''
    consumes an ASCII grid representation and creates a 2D matrix.
    finds the start (sp) and end (ep) points and finds shortest path.
    '''
    maze = Maze()
    maze.print_grid()
    maze.solve()
    solutions = maze.solutions
    for s in solutions:
        print(s)
        maze.print_grid(path=s)
        print()
    shortest = min(solutions, key=len)

    print('Found %s solutions.\n' % len(solutions))
    print('Shortest path (%s steps):' % len(shortest))
    print(shortest)
    maze.print_grid(path=shortest)

if __name__ == "__main__":
    run()
