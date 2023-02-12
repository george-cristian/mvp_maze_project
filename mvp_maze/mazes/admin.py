from django.contrib import admin
from . import models

@admin.register(models.Maze)
class MazeAdmin(admin.ModelAdmin):
    list_display = ('id', 'gridSize')
