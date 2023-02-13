from collections import OrderedDict
import ast
import re
from rest_framework import serializers
from .models import Maze
from . import exceptions


class StringArrayField(serializers.Field):
    """
    String representation of an array field.
    """
    def to_representation(self, obj):
        if isinstance(obj, str):
            obj = ast.literal_eval(obj)
        
        return obj

    def to_internal_value(self, data):
        return data


class MazeSerializer(serializers.ModelSerializer):

    walls = StringArrayField()

    class Meta:
        model = Maze
        fields = ['owner', 'gridSize', 'entrance', 'walls']

    def validate(self, res: OrderedDict):
        grid_size = res.get("gridSize")
        entrance = res.get("entrance")
        walls = res.get("walls")

        self._validate_input_format(grid_size, entrance, walls)

        self._validate_matrix_format(grid_size, entrance, walls)

        return res

    def _validate_input_format(self, grid_size, entrance, walls):
        grid_size_pattern = r"^[A-Z][1-9][0-9]*$"
        element_pattern = r"^[1-9][0-9]*x[1-9][0-9]*$"

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
        grid_size_list = grid_size.split('x')

        nr_cols = int(grid_size_list[0])
        nr_rows = int(grid_size_list[1])

        if nr_cols <= 0 or nr_rows <= 0:
            raise exceptions.InvalidGridSizeException

        bottom_edge_columns = [0] * nr_cols

        for wall in walls:
            wall_col = ord(wall[0]) - 65
            wall_row = int(wall[1:]) - 1

            if wall_col < 0 or wall_col >= nr_cols:
                raise exceptions.InvalidWallException

            if wall_row < 0 or wall_row >= nr_rows:
                raise exceptions.InvalidWallException

            if wall_row == nr_rows - 1:
                bottom_edge_columns[wall_col] = 1

        if all(elem == 1 for elem in bottom_edge_columns):
            raise exceptions.ThereIsNoExitException

