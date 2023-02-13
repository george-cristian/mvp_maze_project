# mvp_maze_project
A Python Django REST API used for creating and retrieving solutions for mazes.

* The users can register using the /register endpoint
* The users can login using the /login endpoint. Once the user logs in, the API responds with a token (using Knox). All API endpoints require a valid token to be supplied in order to access them.

* The user can create mazes via the /maze endpoint using POST. A maze can have the following fields:
1. gridSize - size of the maze (ex:9x9)
2. walls - a list of cells which will represent a wall in the given grid (ex: ["A1", "B2", "C2"])
3. entrance - a cell where the path should being (ex: "A1")

* A user can check his created mazes using the GET method on the /maze endpoint. Or it can retrieve a specific maze using /maze/{mazeId}/

* The user can retrieve a solution to one of the mazes by using GET on the /maze/{mazeId}/solution. The endpoint requires a query parameter "steps" which can be either min or max
1. The API will return a list of cells which represents the path from the entrance to the exit
2. The exit is located on the bottom edge of the grid
3. If steps parameter is min, the API returns the shortest path
4. If steps parameter is max, the API returns the longest path

* Notes:
1. The moves are only horizontally or vertically, not diagonally
2. If the maze has no solution, an error will be thrown
3. The maze can have only one possible exit point, otherwise an error is thrown
