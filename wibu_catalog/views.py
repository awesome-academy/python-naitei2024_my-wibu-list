from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.contrib.auth import authenticate, login as auth_login
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.hashers import check_password
from .models import Users


# import data from constants.py
from wibu_catalog.constants import Role_dict, Score_dict, ITEMS_PER_PAGE_MORE
from wibu_catalog.constants import ITEMS_PER_PAGE, Content_category
from wibu_catalog.constants import Manga_status, Anime_status
from wibu_catalog.constants import Manga_rating, Anime_rating
from wibu_catalog.constants import FIELD_MAX_LENGTH_S, FIELD_MAX_LENGTH_M
from wibu_catalog.constants import FIELD_MAX_LENGTH_L, FIELD_MAX_LENGTH_XL

# import models form models.py
from wibu_catalog.models import Content, Score, Users, FavoriteList
from wibu_catalog.models import ScoreList, Comments, Notifications
from wibu_catalog.models import Product, Order, OrderItems, Feedback

def homepage(request):
    return render(request, 'html/homepage.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('homepage')
    else:
        form = RegistrationForm()
    return render(request, 'html/registerform.html', {'form': form})


# Class definition:
class AnimeListView(generic.ListView):
    """Class for the view of the book list."""
    model = Content
    context_object_name = "anime_list"
    paginate_by = ITEMS_PER_PAGE_MORE
    template_name = "html/anime_list.html"

    def get_queryset(self):
        return Content.objects.filter(category="anime")


class AnimeDetailView(generic.DetailView):
    model = Content
    context_object_name = "anime_detail"
    template_name = "html/anime_detail.html"

    # passing Score to view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_instance = self.get_object()
        score_data_ = content_instance.score_data.all()
        context['score_'] = score_data_
        return context


class MangaListView(generic.ListView):
    """Class for the view of the book list."""
    model = Content
    paginate_by = ITEMS_PER_PAGE_MORE
    context_object_name = "manga_list"
    template_name = "html/manga_list.html"

    def get_queryset(self):
        return Content.objects.filter(category='manga').all()


class MangaDetailView(generic.DetailView):
    model = Content
    context_object_name = "manga_detail"
    template_name = "html/manga_detail.html"

    # passing Score to view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_instance = self.get_object()
        score_data_ = content_instance.score_data.all()
        context['score_'] = score_data_
        return context
    
def authenticate_user(email, password):
    try:
        user = Users.objects.get(email=email)
        if password==user.password:
            return user
        else:
            return None
    except Users.DoesNotExist:
        return None

def login(request):
    check = 1
    if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate_user(email=email, password=password)
            if user is not None:
                return render(request, 'html/homepage_user.html',{'user': user})
            else:
                form = LoginForm()
                check = 0
    else:
        form = LoginForm()
    return render(request, 'html/loginform.html', {'form': form, 'check': check})

#Reset passwword

class PasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'

