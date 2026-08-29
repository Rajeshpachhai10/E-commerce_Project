from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_uuid", "user", "total_amount", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("transaction_uuid", "transaction_code", "user__username", "user__email")
    readonly_fields = ("transaction_uuid", "created_at", "updated_at")