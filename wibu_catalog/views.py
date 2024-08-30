# Python Standard Library
import json
import uuid
from enum import Enum
from functools import wraps
from random import randint

# Django Core and Utilities
from django.contrib import messages
# Django Authentication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods, require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic, View
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse

# Django Authentication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password, make_password

# Import data from constants.py
from wibu_catalog.constants import (
    Role_dict, Score_dict, ITEMS_PER_PAGE_MORE, ITEMS_PER_PAGE,
    Content_category, Manga_status, Anime_status, Manga_rating, Anime_rating,
    FIELD_MAX_LENGTH_S, FIELD_MAX_LENGTH_M,
    FIELD_MAX_LENGTH_L, FIELD_MAX_LENGTH_XL, AVAILABLE_SIZES,
    TOP_WATCHING_LIMIT, LATEST_CONTENT_LIMIT, TOP_RANKED_LIMIT, ScoreEnum,
    PRODUCTS_PER_PAGE_DETAIL, COMMENTS_PER_PAGE_DETAIL,
)
# Import from forms.py
from wibu_catalog.forms import (
    LoginForm, ChangePasswordForm, UserRegistrationForm,
    CommentForm, EditCommentForm, ReplyForm,
)


def _get_user_from_session(request):
    user_id = request.session.get("user_id")
    if user_id:
        try:
            return Users.objects.get(uid=user_id)
        except Users.DoesNotExist:
            return None
    return None


def homepage(request):
    userr = _get_user_from_session(request)
    top_watching_content = Content.objects.order_by("-watching")[
        :TOP_WATCHING_LIMIT
    ]

    latest_content = Content.objects.order_by("-lastUpdate")[
        :LATEST_CONTENT_LIMIT
    ]

    top_ranked_content = Content.objects.order_by("ranked")[:TOP_RANKED_LIMIT]

    what_to_watch = random_button()

    return render(
        request,
        "html/homepage.html",
        {
            "top_watching_content": top_watching_content,
            "latest_content": latest_content,
            "top_ranked_content": top_ranked_content,
            "userr": userr,
            "what_to_watch": what_to_watch,
        },
    )


def random_button():
    """Give random content cid"""
    what_to_watch = None
    while (what_to_watch is None):
        rand_range = Content.objects.count()
        content_random = randint(1, rand_range)
        try:
            what_to_watch = Content.objects.get(cid=content_random)
        except ObjectDoesNotExist:
            what_to_watch = None
    return what_to_watch


def user(request):
    top_watching_content = Content.objects.order_by("-watching")[
        :TOP_WATCHING_LIMIT
    ]

    latest_content = Content.objects.order_by("-lastUpdate")[
        :LATEST_CONTENT_LIMIT
    ]

    top_ranked_content = Content.objects.order_by("ranked")[:TOP_RANKED_LIMIT]

    return render(
        request,
        "html/homepage_user.html",
        {
            "top_watching_content": top_watching_content,
            "latest_content": latest_content,
            "top_ranked_content": top_ranked_content,
        },
    )


class UserRegistrationView(View):
    template_name = 'html/registerform.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")
        dateOfBirth = request.POST.get("dateOfBirth")

        if Users.objects.filter(email=email).exists():
            form.add_error('email', _('Email address already exists.'))
            return render(request, self.template_name, {'form': form})

        if password != password_confirmation:
            form.add_error(
                'password_confirmation', _('Passwords do not match.')
            )
            return render(request, self.template_name, {'form': form})

        new_uid = Users.objects.count() + 1
        user = Users.objects.create(
            uid=new_uid,
            username=name,
            role='new_user',
            email=email,
            password=make_password(password),
            dateOfBirth=dateOfBirth,
            registrationDate=timezone.now(),
        )

        return redirect('login')

# Comment section:
def post_comment(request, content_id):
    userr = _get_user_from_session(request)
    cmtedContent = get_object_or_404(Content, cid=content_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.cid = cmtedContent
            comment.uid = userr
            comment.dateOfCmt = timezone.now().date()
            comment.save()
            return redirect("anime_detail", pk=content_id)
    return redirect("anime_detail", pk=content_id)


def edit_comment(request, comment_id):
    userr = _get_user_from_session(request)
    try:
        comment = Comments.objects.get(id=comment_id, uid=userr.uid)
    except Comments.DoesNotExist:
        return redirect("anime_detail", pk=comment.cid.cid)

    if request.method == "POST":
        form = EditCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment.dateOfCmt = timezone.now().date()  # Update the date
            comment.save()
            return redirect("anime_detail", pk=comment.cid.cid)
            # somehow comment.cid = Content.__str__
    else:
        form = EditCommentForm(instance=comment)

    return redirect("anime_detail", pk=comment.cid.cid)


def delete_comment(request, comment_id):
    try:
        comment = Comments.objects.get(id=comment_id)
        comment.delete()
    except Comments.DoesNotExist:
        return redirect("anime_detail", pk=comment.cid.cid)
    return redirect("anime_detail", pk=comment.cid.cid)


# end of Comment section
def search_content(request):
    userr = _get_user_from_session(request)
    query = request.GET.get("q", "").lower()
    search_results = Content.objects.all()
    if query:
        search_results = search_results.filter(name__icontains=query)

    return render(
        request,
        "html/search_content_results.html",
        {
            "search_results": search_results,
            "userr": userr,
        },
    )


# Class definition:
class AnimeListView(generic.ListView):
    """Class based view for anime list."""

    model = Content
    context_object_name = "anime_list"
    paginate_by = ITEMS_PER_PAGE_MORE
    template_name = "html/anime_list.html"

    def get_queryset(self):
        return Content.objects.filter(category="anime")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userr = _get_user_from_session(self.request)
        context["userr"] = userr
        return context


class AnimeDetailView(generic.DetailView):
    """Class based view for anime detail."""

    model = Content
    context_object_name = "anime_detail"
    template_name = "html/anime_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_instance = self.get_object()
        score_data_ = content_instance.score_data.all()
        userr = _get_user_from_session(self.request)

        # comments related
        comments_list = Comments.objects.\
            filter(cid=content_instance.cid).order_by('-dateOfCmt')
        comments_paginator = Paginator(comments_list, COMMENTS_PER_PAGE_DETAIL)
        comments_page_number = self.request.GET.get("comments_page")
        comments = comments_paginator.get_page(comments_page_number)
        liked_comments = {
            comment.id
            for comment in comments
            if self.request.user in comment.userLikes.all()}

        # Random content button related
        what_to_watch = random_button()

        # Product related
        products = None
        products_list = Product.objects.\
            filter(cid=content_instance.cid).order_by("-ravg")
        if products_list:
            products_paginator = Paginator(
                products_list,
                PRODUCTS_PER_PAGE_DETAIL
            )
            products_page_number = self.request.GET.get("product_page")
            products = products_paginator.get_page(products_page_number)
        else:
            product = None

        # user's favorite status
        favorite = None
        if userr:
            favorite = FavoriteList.objects.filter(
                uid=userr, cid=content_instance
            ).first()

        # User score
        if userr is not None:
            score_str = score_to_str(content_instance.cid, userr.uid)
        else:
            score_str = None

        # Handle reply form
        reply_form = ReplyForm()

        # Sumarize context
        context["score_"] = score_data_
        context["userr"] = userr
        context["comments"] = comments
        context["score_str"] = score_str
        context["favorite"] = favorite
        context["what_to_watch"] = what_to_watch
        context["products"] = products
        context["liked_comments"] = liked_comments
        context['reply_form'] = reply_form
        return context


class MangaListView(generic.ListView):
    """Class for the view of the book list."""

    model = Content
    paginate_by = ITEMS_PER_PAGE_MORE
    context_object_name = "manga_list"
    template_name = "html/manga_list.html"

    def get_queryset(self):
        return Content.objects.filter(category="manga").all()


class MangaDetailView(generic.DetailView):
    model = Content
    context_object_name = "manga_detail"
    template_name = "html/manga_detail.html"

    # passing Score to view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_instance = self.get_object()
        score_data_ = content_instance.score_data.all()
        context["score_"] = score_data_
        return context


def list_product(request):
    userr = _get_user_from_session(request)
    query = request.GET.get(
        "q", ""
    )  # Lấy từ khóa tìm kiếm từ URL, mặc định là chuỗi rỗng
    sort_by = request.GET.get("sort_by", "id")  # Giá trị mặc định là 'id'

    # Tìm kiếm sản phẩm theo từ khóa
    if query:
        products_list = Product.objects.filter(name__icontains=query)
    else:
        products_list = Product.objects.all()

    if sort_by == 'highest_rate':
        products_list = products_list.order_by('-ravg')
    elif sort_by == 'low_to_high':
        products_list = products_list.order_by('price')
    elif sort_by == 'high_to_low':
        products_list = products_list.order_by('-price')

    paginator = Paginator(products_list, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    return render(
        request,
        "html/warehouse.html",
        {
            "products": products,
            "current_sort": sort_by,
            "query": query,
            "userr": userr,
            "paginator": paginator
        },
    )


def filter_by_genre(request, genre):
    userr = _get_user_from_session(request)

    # Lọc content theo thể loại và sắp xếp theo scoreAvg
    filtered_content = Content.objects.filter(genres__icontains=genre).order_by(
        "-scoreAvg"
    )[:ITEMS_PER_PAGE]

    context = {
        "filtered_content": filtered_content,
        "selected_genre": genre,
        "userr": userr,
    }
    return render(request, "html/filtered_content.html", context)


class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            form.add_error("email", _("Email does not exist."))
            return render(request, "html/loginform.html", {"form": form})

        if not check_password(password, user.password):
            form.add_error("password", _("Incorrect password."))
            return render(request, "html/loginform.html", {"form": form})

        request.session["user_id"] = user.uid
        return redirect("homepage")

    def get(self, request):
        form = LoginForm()
        return render(request, "html/loginform.html", {"form": form})


class FavoriteListView(generic.ListView):
    """Class based view for favorite anime list."""

    model = Content
    context_object_name = "favorites_list"
    paginate_by = ITEMS_PER_PAGE_MORE
    template_name = "html/favorites_list.html"

    def get_queryset(self):
        userr = _get_user_from_session(self.request)
        if userr:
            favorite_content_cids = FavoriteList.objects.filter(
                uid=userr
            ).values_list("cid", flat=True)
            return Content.objects.filter(cid__in=favorite_content_cids)
        return FavoriteList.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userr = _get_user_from_session(self.request)
        context["userr"] = userr
        return context


def require_login(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        userr = _get_user_from_session(request)
        if not userr:
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


@require_login
def user_profile(request):
    user_id = request.session.get('user_id')
    try:
        userr = Users.objects.get(uid=user_id)
    except Users.DoesNotExist:
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username')
        date_of_birth = request.POST.get('dateOfBirth')

        # Update
        userr.username = username
        userr.dateOfBirth = date_of_birth
        userr.save()

        messages.success(request, _('Profile updated successfully!'))
        return redirect('user_profile')

    return render(request, 'html/user_profile.html', {'userr': userr})


@require_login
def update_favorite_status(request, content_id):
    userr = _get_user_from_session(request)
    if not userr:
        return HttpResponseForbidden(
            _("You must be logged in to update your status.")
        )

    content_instance = get_object_or_404(Content, cid=content_id)

    status = request.POST.get("status")

    if status in ["1", "2", "3", "5", "6"]:
        favorite, created = FavoriteList.objects.get_or_create(
            uid=userr,
            cid=content_instance,
        )
        favorite.status = status
        favorite.save()
    else:
        FavoriteList.objects.filter(uid=userr, cid=content_instance).delete()

    return redirect("anime_detail", pk=content_id)


def logout(request):
    request.session.flush()
    return redirect("homepage")


def order_history(request):
    userr = _get_user_from_session(request)
    orders = Order.objects.filter(uid_id=uuid)
    return render(
        request, "html/order_history.html", {"orders": orders, "userr": userr}
    )


def product_detail(request, pid=None):
    userr = _get_user_from_session(request)
    product = Product.objects.get(pid=pid)
    cart = request.session.get("cart", [])
    product_quantity_in_cart = 0
    for item in cart:
        if item.get("product_id") == str(product.pid):
            product_quantity_in_cart = item.get("quantity", 0)
            break
    return render(
        request,
        "html/product_detail.html",
        {
            "product": product,
            "userr": userr,
            "available_sizes": AVAILABLE_SIZES,
            "product_quantity_in_cart": product_quantity_in_cart,
        },
    )


@ensure_csrf_cookie  # Ensures the CSRF token is set for the session
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        quantity = int(data.get("quantity", 1))  # Convert quantity to int

        try:
            product = Product.objects.get(pid=product_id)
            cart = request.session.get("cart", [])
            found = False

            for item in cart:
                if item["product_id"] == product_id:
                    item["quantity"] += quantity
                    found = True
                    # Update subtotal for existing item
                    item["subtotal"] = item["quantity"] * product.price
                    break

            if not found:
                cart.append(
                    {
                        "product_id": product_id,
                        "quantity": quantity,
                        "subtotal": product.price
                        * quantity,  # Calculate subtotal for new item
                    }
                )

            # Update the cart total in the session
            request.session["cart_total"] = sum(
                item.get("subtotal", 0) for item in cart
            )
            request.session["cart"] = cart

            return JsonResponse(
                {"success": True, "cart_total": request.session["cart_total"]}
            )

        except Product.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Product not found."}
            )
    else:
        return JsonResponse(
            {"success": False, "error": "Invalid request method."}
        )


@csrf_exempt
@require_POST
def remove_from_cart(request):
    try:
        item_id = int(request.POST.get("item_id"))
        cart_items = request.session.get("cart", [])

        item_to_remove = next((item for item in cart_items if item["product_id"] == item_id), None)

        if item_to_remove is not None:
            cart_items.remove(item_to_remove)
            cart_total = _calculate_cart_total(cart_items)
            request.session["cart"] = cart_items
            request.session["total"] = cart_total
            return JsonResponse({"success": True, "total": cart_total}, status=200)
        else:
            return JsonResponse({
                "success": False,
                "error": f"Item with id {item_id} does not exist in the cart."
            }, status=400)

    except ValueError:
        return JsonResponse({"success": False, "error": "Invalid item ID."}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=200)



def get_product_price(product_id):
    try:
        product = Product.objects.get(pid=product_id)
        return product.price
    except Product.DoesNotExist:
        raise ObjectDoesNotExist("Product not found")


@csrf_exempt
def update_quantity(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        cart = request.session.get("cart", [])
        checked = request.POST.get("checked") == "true"
        if product_id is None:
            return JsonResponse(
                {"success": False, "error": "Product ID is missing"}, status=400
            )

        try:
            product = Product.objects.get(pid=product_id)
        except Product.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Product does not exist"},
                status=404,
            )

        if quantity <= 0 or quantity > product.inventory:
            return JsonResponse(
                {"success": False, "error": "Invalid quantity"}, status=400
            )


        # Get the price of the product
        price = get_product_price(product_id)
        if price is None:
            return JsonResponse(
                {
                    "error": "Product with id {} does not exist".format(
                        product_id
                    )
                },
                status=400,
            )

        # Update the quantity in the session
        for item in cart:
            if item["product_id"] == product_id:
                item["quantity"] = quantity
                item["checked"] = checked
                item["subtotal"] = price * item["quantity"]
                break

        # Calculate the new total
        new_total = sum(
            item["quantity"] * get_product_price(item["product_id"])
            for item in cart
            if get_product_price(item["product_id"]) is not None
        )
        request.session["total"] = new_total
        request.session["cart"] = cart
        print(cart)
        request.session.modified = True  # Ensure session is updated
        return JsonResponse(
            {"new_subtotal": item["subtotal"], "new_total": new_total}
        )

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
@require_POST
def update_cart_item(request):
    item_id = request.POST.get("product_id")
    checked = request.POST.get("checked", "true").lower() == "true"
    cart_items = request.session.get("cart", [])


    for item in cart_items:
        if item["product_id"] == item_id:
            item["checked"] = checked
            try:
                product = Product.objects.get(pid=item["product_id"])
                if item:
                    item["subtotal"] = product.price * item["quantity"]
                else:
                    return JsonResponse({"error": "Item not found"}, status=404)
            except Product.DoesNotExist:
                return JsonResponse(
                    {"success": False, "error": "Product not found"}
                )
            break
    request.session["cart"] = cart_items
    cart_total = _calculate_cart_total(cart_items)
    return JsonResponse(
        {
            "success": True,
            "item_subtotal": item["subtotal"],
            "cart_total": cart_total,
            "subtotal": item["subtotal"],
        }
    )

def _calculate_cart_total(cart_items):
    total = 0
    for item in cart_items:
        if item.get("checked", True):
            total += item["subtotal"]
    return total


def cart(request):
    userr = _get_user_from_session(request)
    """Display the shopping cart page."""
    cart_items = request.session.get("cart", [])
    cart_total = 0  # Initialize cart total
    valid_cart_items = []  # To store valid cart items

    for item in cart_items:
        try:
            product = Product.objects.get(
                pid=item["product_id"]
            )  # Fetch the product
            item["product"] = product  # Attach product details to the item
            item["subtotal"] = (
                product.price * item["quantity"]
            )  # Calculate subtotal
            cart_total += item["subtotal"]  # Add to cart total
            valid_cart_items.append(item)  # Keep valid items
        except Product.DoesNotExist:
            # Log or handle the case where the product does not exis
            continue  # Skip this item since it does not exist
    context = {
        "cart_items": valid_cart_items,  # Use only valid cart items
        "cart_total": cart_total,
        "userr": userr,
    }
    return render(request, "html/cart.html", context)


@require_http_methods(["GET", "POST"])
def checkout(request):
    userr = _get_user_from_session(request)
    if request.method == "POST":
        cart_items = request.session.get("cart", [])
        cart_total = 0  # Initialize cart total

        for item in cart_items:
            if item.get("checked"):
                try:
                    product = Product.objects.get(
                        pid=item["product_id"]
                    )  # Fetch the product
                    item["subtotal"] = (
                        product.price * item["quantity"]
                    )  # Calculate subtotal
                    cart_total += item["subtotal"]  # Add to cart total
                except Product.DoesNotExist:
                    continue  # Skip this item since it does not exist

        # Save user information to session
        customer_info = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "address": request.POST.get("address"),
            "phone": request.POST.get("phone"),
            "city": request.POST.get("city"),
            "country": request.POST.get("country"),
            "email": request.POST.get("email"),
        }

        request.session["customer_info"] = customer_info
        request.session.modified = True  # Ensure session is updated

        context = {
            "cart_items": [item for item in cart_items if item.get("checked")],
            "cart_total": cart_total,
            "userr": customer_info,  # Pass customer_info into context
        }
        return render(request, "html/checkout.html", context)

    elif request.method == "GET":
        cart_items = request.session.get("cart", [])
        cart_total = 0
        print(cart_items)
        for item in cart_items:
            if item.get("checked"):
                try:
                    product = Product.objects.get(pid=item["product_id"])
                    item["subtotal"] = product.price * item["quantity"]
                    cart_total += item["subtotal"]
                except Product.DoesNotExist:
                    cart_items.remove(item)  # Remove invalid item

        customer_info = request.session.get("customer_info", {})
        context = {
            "cart_items": cart_items,
            "cart_total": cart_total,
            "userr": userr,
            "customer_info": customer_info,
        }
        return render(request, "html/checkout.html", context)

def order_confirmation(request):
    userr = _get_user_from_session(request)

    # Tạo đơn order
    order = Order.objects.create(
        uid=userr,
        orderDate=timezone.now(),  # Sử dụng 'orderDate' để lưu trữ
        status="Pending",  # Gán trạng thái mặc định
    )

    # Lấy thông tin từ session `customer_info`
    customer_info = request.session.get("customer_info", {})

    shipping_address = {
        "full_name": (
            f"{customer_info.get('first_name', '')} "
            f"{customer_info.get('last_name', '')}"
        ),
        "address": customer_info.get("address", ""),
        "phone": customer_info.get("phone", ""),
        "city": customer_info.get("city", ""),
        "country": customer_info.get("country", ""),
    }

    # Lấy thông tin từ session `cart`
    cart_items = request.session.get("cart", [])

    # Xử lý các item trong giỏ cart
    valid_cart_items = []
    cart_total = 0

    for item in cart_items:
        if item.get("checked"):
            try:
                product = Product.objects.get(pid=item["product_id"])
                if "subtotal" not in item:
                    item["subtotal"] = product.price * item["quantity"]
                cart_total += item["subtotal"]
                item["product_id"] = product.pid  # Thêm id của Product vào item
                item["product_name"] = product.name  # Thêm tên của Product vào item
                valid_cart_items.append(item)  # Thêm item hợp lệ vào danh sách

                # Lưu thông tin OrderItems vào database
                OrderItems.objects.create(
                    oid=order,  # Liên kết với đơn order vừa tạo
                    pid=product,  # Liên kết với sản phẩm
                    quantity=item["quantity"],  # Số lượng
                    buyPrice=product.price,  # Giá sản phẩm
                )
                cart_items = [i for i in cart_items if not i.get("checked", False)]
            except Product.DoesNotExist:
                pass
        request.session["cart"] = cart_items
        request.session.modified = True
    context = {
        "userr": userr,
        "shipping_address": shipping_address,
        "cart_items": valid_cart_items,
        "cart_total": cart_total,
        "order": order,
    }

    return render(request, "html/order_confirmation.html", context)


@require_login
def update_score(request, content_id):
    """Function to add or update content score rated by user"""
    userr = _get_user_from_session(request)
    if not userr:
        return HttpResponseForbidden(
            _("You must be logged in to rate or update rated score.")
        )

    content_instance = get_object_or_404(Content, cid=content_id)

    if request.method == "POST":
        score, created = ScoreList.objects.get_or_create(
            uid=userr,
            cid=content_instance,
        )
        score.score = request.POST.get("score")
        score.save()

    return redirect("anime_detail", pk=content_id)


def score_to_str(content_cid, user_uid):
    """Convert score int to a sentence"""
    try:
        user_score = ScoreList.objects.get(cid=content_cid, uid=user_uid)
        score_int = user_score.score
        return ScoreEnum(str(score_int)).value
    except ObjectDoesNotExist:
        return None


class ChangePassword(View):
    def post(self, request):
        form = ChangePasswordForm(request.POST)
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_confirmation = request.POST.get(
            "new_password_confirmation"
        )
        userr = _get_user_from_session(request)
        if not check_password(old_password, userr.password):
            form.add_error(
                "old_password", _("Incorrect password")
            )
            return render(
                            request,
                            "html/change_password.html",
                            {"form": form}
                        )
        if new_password != new_password_confirmation:
            form.add_error(
                "new_password_confirmation", _("Passwords do not match.")
            )
            return render(
                            request,
                            "html/change_password.html",
                            {"form": form}
                        )

        userr.password = make_password(new_password)
        userr.save()
        return redirect("homepage")

    def get(self, request):
        form = ChangePasswordForm()
        return render(request, "html/change_password.html", {"form": form})


# Comment section:
@require_login
def post_comment(request, content_id):
    userr = _get_user_from_session(request)
    cmtedContent = get_object_or_404(Content, cid=content_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.cid = cmtedContent
            comment.uid = userr
            comment.dateOfCmt = timezone.now().date()
            comment.save()
            return redirect('anime_detail', pk=content_id)
    return redirect('anime_detail', pk=content_id)


@require_login
def edit_comment(request, comment_id):
    userr = _get_user_from_session(request)
    try:
        comment = Comments.objects.get(id=comment_id, uid=userr.uid)
    except Comments.DoesNotExist:
        return redirect("anime_detail", pk=comment.cid.cid)

    if request.method == "POST":
        form = EditCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment.dateOfCmt = timezone.now().date()  # Update the date
            comment.save()
            return redirect("anime_detail", pk=comment.cid.cid)
    else:
        form = EditCommentForm(instance=comment)

    return redirect("anime_detail", pk=comment.cid.cid)


@require_login
def delete_comment(request, comment_id):
    try:
        comment = Comments.objects.get(id=comment_id)
        comment.delete()
    except Comments.DoesNotExist:
        return redirect("anime_detail", pk=comment.cid.cid)
    return redirect("anime_detail", pk=comment.cid.cid)


@require_login
def toggle_like_comment(request, comment_id):
    """Function to update likes in comments"""
    userr = _get_user_from_session(request)
    if request.method == "POST":
        comment = get_object_or_404(Comments, id=comment_id)

        if userr in comment.userLikes.all():
            comment.userLikes.remove(userr)
            if comment.likes >= 1:
                comment.likes += -1
            else:
                comment.likes = 0
        else:
            comment.userLikes.add(userr)
            comment.likes += 1

        comment.save()

        return redirect("anime_detail", pk=comment.cid.cid)
    return HttpResponse(status=405)


@require_login
def reply_comment(request, comment_id):
    userr = _get_user_from_session(request)
    parent_comment = get_object_or_404(Comments, id=comment_id)

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.uid = userr
            reply.cid = parent_comment.cid
            reply.parent = parent_comment
            reply.dateOfCmt = timezone.now().date()
            reply.save()
            return redirect('anime_detail', pk=parent_comment.cid.cid)
        else:
            return redirect("anime_detail", pk=parent_comment.cid.cid)
    return redirect('anime_detail', pk=parent_comment.cid.cid)

# end of Comment section
