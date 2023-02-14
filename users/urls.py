from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path('user/', views.RegisterAPI.as_view(), name='user'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]
