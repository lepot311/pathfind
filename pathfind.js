angular.module('PathfinderApp', [])
  .controller('MazeCtrl', function($scope, $http) {
    $scope.painting = false;
    $scope.original = {};

    $http.get('/maze').success(function(maze) {
      $scope.maze = maze;
    });

    $scope.submit = function(maze) {
      $http.post('/maze/solve', maze)
        .success(function(maze) {
          $scope.original = _($scope.maze).clone();

          _(maze.solutions).each(function(s) {
            s.steps = $scope.steps_in_solution(s).length
          });

          // sort in place
          $scope.maze.solutions = _(maze.solutions).sortBy(function(s) {
            return s.steps
          });

          $scope.maze.solution = maze.solutions[0];
        });
    };

    $scope.steps_in_solution = function(solution) {
      // lame
      var result = _(solution).flatten()
      return _(result).where({ 'type': 'path' });
    };

    $scope.paint = function(cell, e) {
      if ($scope.painting) {
        cell.type = $scope.brush;
        e.preventDefault();
      }
    };

    $scope.startPainting = function(cell, e) {
      $scope.painting = true;
      $scope.brush = cell.type;
      e.preventDefault();

    };

    $scope.stopPainting = function() {
      $scope.painting = false;
    };

    $scope.toggle_wall = function(cell) {
      if (cell.type == 'space') {
        cell.type = 'wall';
      } else if (cell.type == 'wall') {
        cell.type = 'space';
      }
    };

});

