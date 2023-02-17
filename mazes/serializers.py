from collections import OrderedDict
import ast
import re
from rest_framework import serializers
from .models import Maze
from . import exceptions
from .maze_calculator import ASCII_CODE_A


class StringArrayField(serializers.Field):
    """
    String representation of an array field. Used for serializing and
    deserializing a list of strings.
    """
    def to_representation(self, obj):
        """
        Transform the native value into a primitive data type. Converting a string
        to a list of strings.
        """
        if isinstance(obj, str):
            obj = ast.literal_eval(obj)
        
        return obj

    def to_internal_value(self, data):
        """
        Transform the received data to a db value. No need to transform
        the lsit of strings because it is stored in the db as a string already.
        """
        return data


class MazeSerializer(serializers.ModelSerializer):
    """
    Serializer class for a Maze
    """
    walls = StringArrayField()

    class Meta:
        model = Maze
        fields = ['owner', 'gridSize', 'entrance', 'walls']

    def validate(self, res: OrderedDict):
        """
        Validate the given maze.
        """
        grid_size = res.get("gridSize")
        entrance = res.get("entrance")
        walls = res.get("walls")

        self._validate_input_format(grid_size, entrance, walls)

        self._validate_matrix_format(grid_size, entrance, walls)

        return res

    def _validate_input_format(self, grid_size, entrance, walls):
        """
        Validate the formats of the maze configurations, by checking them against
        regular expressions. The function raises the appropriate exception if one
        of the formats does not match.
        :param grid_size: String representing the gridSize field
        :param entrance: String representing the input entrance field
        :param walls: List of strings representing the walls
        """
        # define the regular expressions
        element_pattern = r"^[A-Z][1-9][0-9]*$"
        grid_size_pattern = r"^[1-9][0-9]*x[1-9][0-9]*$"

        grid_size_match = re.search(grid_size_pattern, grid_size)
        if not grid_size_match:
            raise exceptions.InvalidFormatGridSizeException

        entrance_match = re.search(element_pattern, entrance)
        if not entrance_match:
            raise exceptions.InvalidMazeElementException

        for wall in walls:
            element_match = re.search(element_pattern, wall)
            if not element_match:
                raise exceptions.InvalidMazeElementException

    def _validate_matrix_format(self, grid_size, entrance, walls):
        """
        Validate the format of the given maze by performing multiple sanity
        checks. For example, to see if the walls fit withing the given grid,
        or if the bottom edge of matrix contains only walls. The function
        raises the appropriate exception in case one of the checks fails.
        :param grid_size: String identifying the gridSize
        :param walls: List of strings which identify the walls
        """
        grid_size_list = grid_size.split('x')

        nr_cols = int(grid_size_list[0])
        nr_rows = int(grid_size_list[1])

        if nr_cols <= 0 or nr_rows <= 0:
            raise exceptions.InvalidGridSizeException

        bottom_edge_columns = [0] * nr_cols

        entrance_col = ord(entrance[0]) - ASCII_CODE_A
        entrance_row = int(entrance[1:]) - 1

        for wall in walls:
            wall_col = ord(wall[0]) - ASCII_CODE_A
            wall_row = int(wall[1:]) - 1

            if wall_col < 0 or wall_col >= nr_cols:
                raise exceptions.InvalidWallException

            if wall_row < 0 or wall_row >= nr_rows:
                raise exceptions.InvalidWallException

            if entrance_col == wall_col and entrance_row == wall_row:
                raise exceptions.InvalidEntranceException

            if wall_row == nr_rows - 1:
                bottom_edge_columns[wall_col] = 1

        # if there are only walls on the bottom edge, then raise exception because there is no possible exit
        if all(elem == 1 for elem in bottom_edge_columns):
            raise exceptions.ThereIsNoExitException
