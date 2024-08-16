from django.contrib import admin
from .models import Content, Score, Users, FavoriteList
from .models import ScoreList, Comments, Notifications
from .models import Product, Order, OrderItems, Feedback


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 1
    list_display = [
        'pid',
        'product_name',
        'quantity',
        'buyPrice',
        ]
    readonly_fields = list_display

    def has_delete_permission(self, request, obj=None):
        return False  # Disable the delete checkbox

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "oid",
        "orderDate",
        "status",
        "get_username",
        )

    fields = [
        "status",
        ]

    inlines = [OrderItemsInline]

    search_fields = ("oid", "uid__username")  # Allow searching by order ID and user
    list_filter = ("status", "orderDate")  # Add filters for status and date

    def get_username(self, obj):
        return obj.uid.username

    get_username.admin_order_field = 'uid__username'  # Allow sorting by username
    get_username.short_description = 'User'  # Label for the column

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("uid")  # Optimize queries by using select_related
        return queryset
