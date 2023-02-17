from rest_framework.exceptions import APIException
from rest_framework import status


class InvalidFormatGridSizeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid format for gridSize (should be something like 8x8)'
    default_code = 'invalid'


class InvalidMazeElementException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid format for a maze element (should be something like A8 or B1 or C2)'
    default_code = 'invalid'


class InvalidGridSizeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid numbers provided for the grid size. The numbers should be positive integers greater than zero.'
    default_code = 'invalid'


class InvalidWallException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'At least one of the provided walls is outside of the maze size'
    default_code = 'invalid'


class ThereIsNoExitException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The bottom edge of the maze contains only walls, so there is no exit'
    default_code = 'invalid'


class MultipleExitsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Multiple possible exits from the maze were found. The maze should have only one exit point'
    default_code = 'invalid'


class NoExitFoundException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'No exit was found for the given maze'
    default_code = 'invalid'


class InvalidEntranceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The given entrance is a wall'
    default_code = 'invalid'
