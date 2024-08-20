from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.core.paginator import Paginator

from django.db.models import Q
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

from .constants import TOP_WATCHING_LIMIT, LATEST_CONTENT_LIMIT, TOP_RANKED_LIMIT
from wibu_catalog.constants import ITEMS_PER_PAGE

def homepage(request):
    top_watching_content = Content.objects.order_by('-watching')[:TOP_WATCHING_LIMIT]

    latest_content = Content.objects.order_by('-lastUpdate')[:LATEST_CONTENT_LIMIT]

    top_ranked_content = Content.objects.order_by('ranked')[:TOP_RANKED_LIMIT]

    return render(request, 'html/homepage.html', {
        'top_watching_content': top_watching_content,
        'latest_content': latest_content,
        'top_ranked_content': top_ranked_content,
    })


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
def list_product(request):
    query = request.GET.get('q', '')  # Lấy từ khóa tìm kiếm từ URL, mặc định là chuỗi rỗng
    sort_by = request.GET.get('sort_by', 'id')  # Giá trị mặc định là 'id'

    # Tìm kiếm sản phẩm theo từ khóa
    if query:
        products_list = Product.objects.filter(name__icontains=query)
    else:
        products_list = Product.objects.all()

    # Sắp xếp sản phẩm theo yêu cầu
    if sort_by == 'highest_rate':
        products_list = products_list.order_by('-ravg')
    elif sort_by == 'low_to_high':
        products_list = products_list.order_by('price')
    elif sort_by == 'high_to_low':
        products_list = products_list.order_by('-price')

    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'html/warehouse.html', {'products': products, 'current_sort': sort_by, 'query': query})

def search_content(request):
    query = request.GET.get('q','').lower() 
    search_results = None
    if query:
        search_results = Content.objects.filter(name__icontains=query) 
    else:
        search_results = Content.objects.all()  # Nếu không có từ khóa, hiển thị tất cả

    return render(request, 'html/search_content_results.html', {'search_results': search_results,})

def filter_by_genre(request, genre):
    # Lọc content theo thể loại và sắp xếp theo scoreAvg
    filtered_content = Content.objects.filter(genres__icontains=genre).order_by('-scoreAvg')[:ITEMS_PER_PAGE]

    context = {
        'filtered_content': filtered_content,
        'selected_genre': genre  # Truyền thể loại đã chọn để hiển thị trên trang kết quả
    }
    return render(request, 'html/filtered_content.html', context)

