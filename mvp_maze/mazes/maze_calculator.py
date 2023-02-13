import ast
from collections import deque
from . import exceptions

ASCII_CODE_A = 65

class MazeCalculator(object):

    @staticmethod
    def calculate_solution(maze, calculation_type):
        entrance_col = ord(maze.entrance[0]) - ASCII_CODE_A
        entrance_row = int(maze.entrance[1:]) - 1

        matrix = MazeCalculator._convert_maze_to_matrix(maze)

        solution_path = MazeCalculator._find_path_to_exit(matrix, (entrance_col, entrance_row), calculation_type)

        if solution_path is None:
            raise exceptions.NoExitFoundException

        converted_path = []
        converted_path.append(maze.entrance)
        for (row, col) in solution_path:
            converted_col = chr(col + ASCII_CODE_A)
            converted_row = row + 1
            converted_path.append("%s%d" % (converted_col, converted_row))

        return converted_path

    @staticmethod
    def _convert_maze_to_matrix(maze):
        grid_size = maze.gridSize
        grid_size_list = grid_size.split('x')

        nr_cols = int(grid_size_list[0])
        nr_rows = int(grid_size_list[1])

        matrix = [[0 for _ in range(nr_cols)] for _ in range(nr_rows)]
        
        walls = ast.literal_eval(maze.walls)
        for wall in walls:
            wall_col = ord(wall[0]) - ASCII_CODE_A
            wall_row = int(wall[1:]) - 1

            matrix[wall_row][wall_col] = 1

        return matrix    

    @staticmethod
    def _find_path_to_exit(maze, entrance, type):
        # Define possible moves (up, down, left, right)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Define a queue to store nodes to visit and a set to store visited nodes
        queue = deque([(entrance, [])])
        visited = set([entrance])
        
        # Define a variable to store the shortest path found so far
        shortest_path = None
        longest_path = None
        
        # Iterate over the queue until it is empty
        while queue:
            # Dequeue the next node to visit and its path
            curr, path = queue.popleft()
            
            # Check if the current node is on the bottom edge of the maze
            if curr[0] == len(maze) - 1:
                if type == 'min':
                    # If this is the first exit found, set shortest path to it
                    if shortest_path is None:
                        shortest_path = path
                    # Otherwise, update shortest path if necessary
                    else:
                        # Check if the exit point is the same as the already found path. If not, raise a error
                        if path[-1][0] != shortest_path[-1][0] or path[-1][1] != shortest_path[-1][1]:
                            raise exceptions.MultipleExitsException
                        elif len(path) < len(shortest_path):
                            shortest_path = path
                else:
                    # If this is the first exit found, set longest path path to it
                    if longest_path is None:
                        longest_path = path
                    # Otherwise, update shortest path if necessary
                    else:
                        # Check if the exit point is the same as the already found path. If not, raise a error
                        if path[-1][0] != shortest_path[-1][0] or path[-1][1] != shortest_path[-1][1]:
                            raise exceptions.MultipleExitsException
                        elif len(path) > len(longest_path):
                            longest_path = path
            
            # Check all possible moves from the current node
            for move in moves:
                next_node = (curr[0] + move[0], curr[1] + move[1])
                
                # Check if the next node is a valid open path and has not been visited before
                is_next_node_valid = (0 <= next_node[0] < len(maze) and 0 <= next_node[1] < len(maze[0]) and maze[next_node[0]][next_node[1]] == 0)

                if is_next_node_valid and next_node not in visited:
                    # Add the next node and its path to the queue and visited set
                    queue.append((next_node, path + [next_node]))
                    visited.add(next_node)
        
        result_path = None
        if type == 'min':
            result_path = shortest_path
        else:
            result_path = longest_path

        return result_path
