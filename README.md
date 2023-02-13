# mvp_maze_project
A Python Django REST API used for creating and retrieving solutions for mazes.

* The users can register using the /regiser endpoint
* The users can login using the /login endpoint. Once the user logs in, the API responds with a token (using Knox). All API endpoints require a valid token to be supplied in order to access them.
* The user can create mazes via the /maze endpoint using POST. A maze can have the following fields:
** gridSize - size of the maze (ex:9x9)
** walls - a list of cells which will represent a wall in the given grid (ex: ["A1", "B2", "C2"])
** entrance - a cell where the path should being (ex: "A1")
* A user can check his created mazes using the GET method on the /maze endpoint. Or it can retrieve a specific maze using /maze/<mazeId>/
* The user can retrieve a solution to one of the mazes by using GET on the /maze/<mazeId>/solution. The endpoint requires a query parameter "steps" which can be either min or max
** The API will return a list of cells which represents the path from the entrance to the exit
*** The exit is located on the bottom edge of the grid
*** If steps parameter is min, the API returns the shortest path
*** If steps parameter is max, the API returns the longest path
** Notes:
*** The moves are only horizontally or vertically, not diagonally
*** If the maze has no solution, an error will be thrown
*** The maze can have only one possible exit point, otherwise an error is thrown
