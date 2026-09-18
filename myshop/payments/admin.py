from django.contrib import admin

from .models import Order, OrderItem, Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_uuid", "user", "total_amount", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("transaction_uuid", "transaction_code", "user__username", "user__email")
    readonly_fields = ("transaction_uuid", "created_at", "updated_at")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_id", "name", "price", "quantity", "image")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "created_at")
    search_fields = ("user__username", "user__email", "transaction__transaction_uuid")
    inlines = [OrderItemInline]