from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    # url mapping for list views
    path('anime/', views.AnimeListView.as_view(), name='anime'),
    path('manga/', views.MangaListView.as_view(), name='manga'),

    # url mapping for detail views
    path('anime/<int:pk>', views.AnimeDetailView.as_view(), name='anime_detail'),
    path('manga/<int:pk>', views.MangaDetailView.as_view(), name='manga_detail'),
    #url mapping for warehouse views
    path('product/',views.list_product,name='product'),
    path('search_content/', views.search_content, name='search_content'),
    path('filter_by_genre/<str:genre>/', views.filter_by_genre, name='filter_by_genre'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),

]
