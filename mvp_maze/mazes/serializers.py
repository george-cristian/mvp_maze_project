from rest_framework import serializers
from .models import Maze
import ast


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

    class Meta:
        model = Maze
        fields = ['owner', 'gridSize', 'entrance', 'walls']

    walls = StringArrayField()
