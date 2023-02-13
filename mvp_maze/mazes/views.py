from .serializers import MazeSerializer
from .models import Maze
from .maze_calculator import MazeCalculator
from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action

class MazeViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  viewsets.GenericViewSet):
    
    permission_classes = (IsAuthenticated, )
    serializer_class = MazeSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return Maze.objects.filter(owner=user)

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = MazeSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                maze = Maze.objects.create(
                    owner=request.user,
                    gridSize=data['gridSize'],
                    entrance=data['entrance'],
                    walls=data['walls']
                )
                return Response(MazeSerializer(maze).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def solution(self, request, *args, **kwargs):
        steps = request.GET.get('steps', '')
        if not steps or steps not in ['min', 'max']:
            return Response("Please provide a valid steps query parameter", status=status.HTTP_400_BAD_REQUEST)
        else:
            maze_obj = Maze.objects.get(id=kwargs['id'])
            response = None
            try:
                result = MazeCalculator.calculate_solution(maze_obj, steps)
                response = JsonResponse({"path": result}, status=status.HTTP_200_OK)
            except ValueError as exc:
                response = JsonResponse({"error_message": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

            return response
            