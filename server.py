import json
import logging
from flask import Flask, request
import pathfind

app = Flask(__name__)


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class ServerMaze(pathfind.Maze):
    type_map = {
        'space': ' ',
        'wall':  '|',
        'start': 'S',
        'end':   'E',
    }

    def __init__(self, grid=None):
        # TODO: we can improve this
        if grid:
            super().__init__(pic=self.json_to_ascii(grid))
        else:
            super().__init__()

    def json_to_ascii(self, grid):
        text = [[ ServerMaze.type_map[cell['type']] for cell in row  ]
                                                    for row  in grid ]
        output = ''
        for row in text:
            output += ''.join(row) + '\n'

        return '\n'+output

    @property
    def as_json(self):
        result = {}
        result['grid'] = [[ { 'type': cell._type } for cell in row       ]
                                                   for row  in self.grid ]
        solutions = []

        # TODO: probably time to start thinking about making grid and solution classes
        for solution in self.solutions:
            grid = []
            for row in self.grid:
                r = []
                for cell in row:
                    if cell in solution:
                        r.append({ 'type': 'path' })
                    else:
                        r.append({ 'type': cell._type })
                grid.append(r)
            solutions.append(grid)

        result['solutions'] = solutions

        return json.dumps(result)


@app.route('/maze')
def index():
    maze = ServerMaze()
    log.info(f"Serving maze {maze.sha1[:8]}")
    return maze.as_json


@app.route('/maze/solve', methods=['POST'])
def solve():
    grid = json.loads( request.data.decode() )['grid']

    maze = ServerMaze(grid=grid)
    log.info(f"Solving for maze {maze.sha1[:8]}")
    log.debug(str(maze))
    maze.solve()
    log.info(f"Serving maze {maze.sha1[:8]}")

    return maze.as_json



if __name__ == '__main__':
    app.run(port=4000)
