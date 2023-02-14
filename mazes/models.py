from django.db import models
from django.contrib.auth.models import User


class Maze(models.Model):
    """
    Class which defines the model for a Maze
    """
    class Meta:
        verbose_name = 'Maze'
        verbose_name_plural = 'Mazes'
        ordering = ['id']

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    gridSize = models.CharField(max_length=20)
    entrance = models.CharField(max_length=20)
    walls = models.TextField()
