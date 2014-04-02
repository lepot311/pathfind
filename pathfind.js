angular.module('PathfinderApp', [])
  .controller('MazeCtrl', function($scope, $http) {

    $http.get('/maze').success(function(maze) {
      $scope.maze = maze;
    });

    $scope.submit = function(maze) {
      $http.post('/maze/solve', maze)
        .success(function(maze) {

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

});

