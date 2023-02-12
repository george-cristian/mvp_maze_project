from .serializers import MazeSerializer
from .models import Maze
from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

class MazeViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  viewsets.GenericViewSet):
    
    permission_classes = (IsAuthenticated, )
    serializer_class = MazeSerializer

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
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)
