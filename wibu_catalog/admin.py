from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Comments, Content, Order, OrderItems


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 1
    list_display = [
        "pid",
        "product_name",
        "quantity",
        "buyPrice",
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

    search_fields = (
        "oid",
        "uid__username",
    )  # Allow searching by order ID and user
    list_filter = ("status", "orderDate")  # Add filters for status and date

    def get_username(self, obj):
        return obj.uid.username

    get_username.admin_order_field = (
        "uid__username"  # Allow sorting by username
    )
    get_username.short_description = "User"  # Label for the column

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related(
            "uid"
        )  # Optimize queries by using select_related
        return queryset


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "get_username",
        "cid",
        "content",
        "dateOfCmt",
        "likes",
    ]
    search_fields = ("content",)
    list_filter = ("dateOfCmt", "likes")
    ordering = ("-dateOfCmt",)
    readonly_fields = list_display

    def get_username(self, obj):
        return obj.uid.username

    get_username.short_description = "Username"


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("name", "lastUpdate")
    list_filter = ("lastUpdate",)
    search_fields = ("name",)
    fields = ("name", "lastUpdate", "picture")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def get_field_display(self, obj):
        return _("Title: {name} - Last updated: {last_update}").format(
            name=obj.name,
            last_update=obj.lastUpdate
        )
