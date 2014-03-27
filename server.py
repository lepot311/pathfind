import json
from flask import Flask, request
import pathfind

app = Flask(__name__)



@app.route('/solver')
def index():
    maze = pathfind.Maze()
    return json.dumps(maze.as_dict)


@app.route('/solver/solve', methods=['POST'])
def solve():
    grid = json.loads( request.data.decode() )['grid']

    maze = pathfind.Maze()

    maze.grid_from_json(grid)

    maze.solve()

    return json.dumps(maze.as_dict['solutions'])



if __name__ == '__main__':
    app.run(port=4000)
