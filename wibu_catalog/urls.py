from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),

    # url mapping for list views
    path('anime/', views.AnimeListView.as_view(), name='anime'),
    path('manga/', views.MangaListView.as_view(), name='manga'),

    # url mapping for detail views
    path('anime/<int:pk>', views.AnimeDetailView.as_view(), name='anime_detail'),
    path('manga/<int:pk>', views.MangaDetailView.as_view(), name='manga_detail'),
]
