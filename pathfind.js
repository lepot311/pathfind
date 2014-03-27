angular.module('PathfinderApp', [])
  .controller('MazeCtrl', function($scope, $http) {

    $http.get('/solver').success(function(maze) {
      $scope.maze = maze;
    });

    $scope.submit = function(maze) {
      $http.post('/solver/solve', maze)
        .success(function(solutions) {
          $scope.maze.solutions = solutions;
          $scope.maze.solution = solutions[0];
          console.log(solutions[0]);
        });
    };

});

