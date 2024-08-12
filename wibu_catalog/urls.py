from django.urls import path
from . import views
from .views import register, login

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]
