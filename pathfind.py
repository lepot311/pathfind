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

def grid_from_pic(pic):
    '''
    returns a 2D matrix (grid representation) from a multiline ascii string

    strips the first and last lines for better ascii art representation
    '''
    return [[cell for cell in row] for row in pic.split('\n')][1:-1]


class Maze(object):
    def __init__(self, grid):
        self.solutions = []
        self.grid = [[ Cell(self, x, y, char) \
                for x, char in enumerate(row) ]
                    for y, row in enumerate(grid) ]

        for row in self.grid:
            for cell in row:
                if cell.char is 'S':
                    self.starting_point = cell
                elif cell.char is 'E':
                    self.ending_point = cell

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
        return "(%s, %s)" % (self.x, self.y)

    def print_char(self):
        try:
            print(colored(self.char, Cell.colors[self.char]), end='')
        except KeyError:
            print(colored(self.char, 'white'), end='')

    def pathfind(self, path):
        branches = [ n for n in self.neighbors \
                        if n.is_open \
                        and not n in path ]

        for b in branches:
            if b is self.maze.ending_point:
                self.maze.solutions.append(path + [self])
            else:
                b.pathfind(path + [self])

    @property
    def is_open(self):
        return not self.is_wall

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
    grid = grid_from_pic(large_maze)
    maze = Maze(grid)
    maze.print_grid()
    maze.solve()
    solutions = maze.solutions
    shortest = min(solutions, key=len)

    print('Found %s solutions.\n' % len(solutions))
    print('Shortest path (%s steps):' % len(shortest))
    print(shortest)
    maze.print_grid(path=shortest)

if __name__ == "__main__":
    run()
