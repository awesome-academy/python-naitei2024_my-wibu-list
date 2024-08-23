from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import MangaDetailView, AnimeDetailView
from .views import FavoriteListView, AnimeListView, MangaListView
from .views import homepage, register, LoginView, logout
from .views import list_product, search_content, filter_by_genre
from .views import post_comment, edit_comment, delete_comment



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

    # url mapping for login logout
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),

    # url mapping for comment
    path('post_comment/<int:content_id>/', views.post_comment, name='post_comment'),
    path('edit_comment/<str:comment_id>', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    # url mapping for favorite list view
    path('favorites/', views.FavoriteListView.as_view(), name='favorite_list'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('update_favorite_status/<int:content_id>/', views.update_favorite_status, name='update_favorite_status'),

    # url mapping for rating score
    path('update_score/<int:content_id>/', views.update_score, name='update_score'),
]
