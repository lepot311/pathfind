import hashlib
import itertools

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
    ascii_map = {
        ' ': 'space',
        '|': 'wall',
        'S': 'start',
        'E': 'end',
    }

    def __init__(self, pic=large_maze):
        self.solutions = []

        grid = self.grid_from_ascii(pic=pic)

        # TODO: do something smarter..
        self.grid = [[ Cell(self, (x, y), char)
                for x, char in enumerate(row)  ]
                for y, row  in enumerate(grid) ]

    def __str__(self):
        return ''.join([
            str(cell) for cell in self.flattened
        ])

    @property
    def flattened(self):
        return itertools.chain(*self.grid)

    def grid_from_ascii(self, pic):
        '''
        Returns a 2D matrix (grid representation) from a multiline ascii string.
        Strips the first and last lines for better ascii art representation.
        '''
        return [[cell for cell in row] for row in pic.split('\n')][1:-1]

    def print_grid(self, path=None):
        '''
        Prints a pretty representation of the grid to stdout.
        '''
        for row in self.grid:
            print()
            for cell in row:
                if path and cell in path:
                    print(colored('.', 'red'), end='')
                    continue
                print(cell, end='')

    def cell_at(self, x, y):
        return self.grid[y][x]

    def solve(self):
        self.start.pathfind([])

    @property
    def sha1(self):
        h = hashlib.sha1()
        h.update(str(self).encode('utf-8'))
        return h.hexdigest()


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

    def __init__(self, maze, coord, char=''):
        self.maze = maze
        self.coord = coord
        self.char = char

        self.x, self.y = self.coord

        self._type = Maze.ascii_map[self.char]

        # TODO: re-use the class' mapping
        self.start = self.char is 'S'
        self.end =   self.char is 'E'
        self.wall =  self.char is '|'

        if self.start:
            self.maze.start = self

    def __repr__(self):
        return "Cell (%s, %s)" % self.coord

    def __str__(self):
        color = Cell.colors.get(self.char)
        return colored(self.char, color)

    def pathfind(self, path):
        for b in self.choices(path):
            if b.end:
                self.maze.solutions.append(path + [self])
            else:
                b.pathfind(path + [self])

    def choices(self, path):
        '''
        Return Cells that aren't walls and aren't in the path.
        '''
        return [ cell for cell in self.neighbors
                      if not cell.wall
                      and not cell in path ]

    @property
    def neighbors(self):
        '''
        Returns a list of (x, y) tuples for each orthogonally adjacent cell.
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
    Consumes an ASCII grid representation and creates a 2D matrix.
    Finds the start (sp) and end (ep) points and finds shortest path.
    '''
    maze = Maze()
    maze.print_grid()
    maze.solve()
    solutions = maze.solutions
    for s in solutions:
        #print(s)
        maze.print_grid(path=s)
        print()
    shortest = min(solutions, key=len)

    print('Found %s solutions.\n'     % len(solutions))
    print('Shortest path (%s steps):' % len(shortest))
    maze.print_grid(shortest)

if __name__ == "__main__":
    run()
