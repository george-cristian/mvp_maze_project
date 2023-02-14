from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from mazes import views as maze_views

# generate the routing for the maze endpoints
router = routers.DefaultRouter()
router.register(r'maze', maze_views.MazeViewSet, basename='maze')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]
