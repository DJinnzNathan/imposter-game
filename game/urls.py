from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_room, name='create_room'),
    path('join/', views.join_room, name='join_room'),
    path('room/<str:room_name>/', views.room, name='room'),
]
