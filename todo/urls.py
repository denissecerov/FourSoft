from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.my_login, name='my_login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='user_logout'),
    path('create_task/', views.create_task, name='create_task'),
    path('update_task/<int:pk>/', views.update_task, name='update_task'),
    path('delete_task/<int:pk>/', views.delete_task, name='delete_task'),
]