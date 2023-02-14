import ast
from collections import deque
from . import exceptions

ASCII_CODE_A = 65

class MazeCalculator(object):
    """
    Class which contains static functions used for calculating the shortest
    and longest paths in a maze.
    """
    @staticmethod
    def calculate_solution(maze, calculation_type):
        """
        Function which converts a given maze and calculates the path to exit
        using the given type. The solution path is then converted back to
        a format accepted by the API.
        :param maze: Maze object which contains the configuration for the maze
        :param calculation_type: String which defines if the shortest or longest
                                 path should be computed (min or max)
        :return: list of maze points which indicates the solution path
                 Ex: ['A1', 'C1', 'D1']
        """
        # convert the entrance points from string to numbers
        entrance_col = ord(maze.entrance[0]) - ASCII_CODE_A
        entrance_row = int(maze.entrance[1:]) - 1

        # convert the maze configuration to a matrix of ones and zeros
        matrix = MazeCalculator._convert_maze_to_matrix(maze)

        # compute the solution path
        solution_path = MazeCalculator._find_path_to_exit(matrix, (entrance_col, entrance_row), calculation_type)

        if solution_path is None:
            raise exceptions.NoExitFoundException

        # convert back the solution path to a list of strings
        converted_path = []
        for (row, col) in solution_path:
            converted_col = chr(col + ASCII_CODE_A)
            converted_row = row + 1
            converted_path.append("%s%d" % (converted_col, converted_row))

        return converted_path

    @staticmethod
    def _convert_maze_to_matrix(maze):
        """
        Function which converts a maze configuration to a matrix of ones and
        zeros.
        :param maze: A maze object which contains the configuration
        :return: A matrix containing ones (walls) and zeros
        """
        grid_size = maze.gridSize
        grid_size_list = grid_size.split('x')

        nr_cols = int(grid_size_list[0])
        nr_rows = int(grid_size_list[1])

        matrix = [[0 for _ in range(nr_cols)] for _ in range(nr_rows)]
        
        # iterate over the walls and set the position to one in the matrix
        walls = ast.literal_eval(maze.walls)
        for wall in walls:
            wall_col = ord(wall[0]) - ASCII_CODE_A
            wall_row = int(wall[1:]) - 1

            matrix[wall_row][wall_col] = 1

        return matrix    

    @staticmethod
    def _find_path_to_exit(matrix, entrance, search_type):
        """
        Function which calls the appropriate search function based on the
        search type, to compute the maze solution.
        :param matrix: The matrix in which the solution is searched
        :param entrance: The entrance point in the matrix
        :param search_type: The type of search. Either min or max
        :return: The solution path to the maze
        """
        if search_type == "max":
            return MazeCalculator._longest_path_to_bottom(matrix, entrance)
        else:
            return MazeCalculator._shortest_path_to_bottom(matrix, entrance)

    @staticmethod
    def _shortest_path_to_bottom(matrix, entrance):
        """
        Function which searches and computes the shortest path in the matrix.
        It uses the Breadth First Search algorithm (with some adaptations) in
        order to find the shortest path.
        :param matrix: The matrix in which the solution is searched
        :param entrance: The entrance point in the matrix
        """
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        nr_rows, nr_cols = len(matrix), len(matrix[0])

        # Initialize a queue for the BFS algorithm
        queue = deque([entrance])

        # Initialize a dictionary to store and remember all the path lengths from a point
        path_lengths = {entrance: 0}

        # This is a dictionary used to trace back the path from a given point
        predecessors = {}

        # This variable is used to check if there are multiple exit points found
        first_bottom_edge_point = None

        while queue:
            current_point = queue.popleft()
            curr_row, curr_col = current_point

            # If there is a wall in the current point, then continue to the next one
            if matrix[curr_row][curr_col] == 1:
                continue

            # If the bottom edge is reached, continue
            if curr_row == nr_rows - 1:
                if not first_bottom_edge_point:
                    first_bottom_edge_point = current_point
                elif first_bottom_edge_point != current_point:
                    raise exceptions.MultipleExitsException
                continue
            
            # Iterate over all of the possible moves
            for move in moves:
                next_point = (curr_row + move[0], curr_col + move[1])
                # Check if the next point is valid and was not visited
                if (0 <= next_point[0] < nr_rows) and \
                   (0 <= next_point[1] < nr_cols) and \
                    next_point not in path_lengths:
                    # Register the next point in the queue and the visited dictionary and register its predecessor
                    queue.append(next_point)
                    path_lengths[next_point] = path_lengths[current_point] + 1
                    predecessors[next_point] = current_point

        # In case a solution was not found, return None
        if first_bottom_edge_point is None:
            return None

        # Reconstruct the shortest path starting from the solution point
        path = MazeCalculator._reconstruct_path(first_bottom_edge_point, entrance, predecessors)

        return path

    @staticmethod
    def _longest_path_to_bottom(matrix, entrance):
        """
        Function which searches and computes the longest path in the matrix.
        It uses the Depth First Search algorithm (with some adaptations) in
        order to find the longest path.
        :param matrix: The matrix in which the solution is searched
        :param entrance: The entrance point in the matrix
        """
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        nr_rows, nr_cols = len(matrix), len(matrix[0])

        # Initialize a stack to be used in the depth first search algorithm
        stack = [entrance]

        # Dictionary to keep track of the path length for each visited point
        path_lengths = {entrance: 0}

        # Keep track of the point from which we arrived at the current point. Used for reconstructing the path
        predecessors = {}

        # This variable is used to check if there are multiple exit points found
        first_bottom_edge_point = None

        while stack:
            current_point = stack.pop()

            curr_row, curr_col = current_point

            # If there is a wall in the current point, then continue to the next one
            if matrix[curr_row][curr_col] == 1:
                continue
            
            # If the bottom edge is reached, check if there was another possible solution found, otherwise continue
            if curr_row == nr_rows-1:
                if not first_bottom_edge_point:
                    first_bottom_edge_point = current_point
                elif first_bottom_edge_point != current_point:
                    raise exceptions.MultipleExitsException
                continue

            # Iterate over all of the possible moves
            for move in moves:
                next_point = (curr_row + move[0], curr_col + move[1])
                # Check if the next point is valid and was not visited
                if (0 <= next_point[0] < nr_rows) and \
                   (0 <= next_point[1] < nr_cols) and \
                    next_point not in path_lengths:
                    # Register the next point in the stack and the visited dictionary and register its predecessor
                    stack.append(next_point)
                    path_lengths[next_point] = path_lengths[current_point] + 1
                    predecessors[next_point] = current_point

        # In case a solution was not found, return None
        if first_bottom_edge_point is None:
            return None

        # Reconstruct the shortest path starting from the solution point
        path = MazeCalculator._reconstruct_path(first_bottom_edge_point, entrance, predecessors)

        return path
    
    @staticmethod
    def _reconstruct_path(point, entrance, predecessors):
        """
        Helper function which reconstructs a path from a given point to the
        entrance, using its predecessor nodes which are computed by the
        BFS or DFS algorithms.
        :param point: Tuple which defines point from which the path is reconstructed
        :param entrance: Tuple which defines the entrance point
        :param predecessors: Dictionary containing a mapping between the current
                             point and its predecessor, as computed by the BFS
                             or DFS algorithms
        :return: A list of points starting from the entrance point until the given point
        """
        path = []
        while point != entrance:
            path.append(point)
            point = predecessors[point]
        path.append(entrance)
        path.reverse()

        return path
