from django.contrib import admin
from django.utils.html import format_html
from .models import *




admin.site.register(ContactMessage)


# ---------- Reusable inline for extra product photos ----------
class ProductAdminImage(admin.TabularInline):
    model = ProductImage
    extra = 2
    fields = ['image', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px; border-radius:6px;">', obj.image.url)
        return "—"
    image_preview.short_description = "Preview"


# ---------- Custom filter for a continuous field (price) ----------
class PriceRangeFilter(admin.SimpleListFilter):
    title = "price range"
    parameter_name = "price_range"

    def lookups(self, request, model_admin):
        return [
            ("under_1000", "Under Rs. 1,000"),
            ("1000_5000", "Rs. 1,000 – 5,000"),
            ("above_5000", "Above Rs. 5,000"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "under_1000":
            return queryset.filter(price__lt=1000)
        if self.value() == "1000_5000":
            return queryset.filter(price__gte=1000, price__lte=5000)
        if self.value() == "above_5000":
            return queryset.filter(price__gt=5000)
        return queryset


# ---------- Product ----------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'name', 'category', 'subcategory', 'mark_price',
                     'discount_percent', 'price', 'stock_quantity', 'new_badge']
    list_display_links = ['thumbnail']
    list_editable = ['name', 'discount_percent', 'stock_quantity']
    list_filter = ['category', 'subcategory', PriceRangeFilter]
    search_fields = ['name', 'category__title', 'subcategory__title']
    list_per_page = 20
    inlines = [ProductAdminImage]

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px; border-radius:6px;">', obj.image.url)
        return "—"
    thumbnail.short_description = "Image"

    def new_badge(self, obj):
        if obj.is_new():
            return format_html('<span style="color:green; font-weight:bold;">{}</span>', "New")
        return ""
    new_badge.short_description = "Status"


# ---------- Category ----------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'subcategory_count']
    search_fields = ['title']

    def subcategory_count(self, obj):
        return obj.subcategory_set.count()
    subcategory_count.short_description = "Subcategories"


# ---------- SubCategory ----------
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    list_filter = ['category']
    search_fields = ['title', 'category__title']


# ---------- OfferProduct ----------
@admin.register(OfferProduct)
class OfferProductAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'title', 'price', 'is_available', 'created_at']
    list_display_links = ['thumbnail']
    list_editable = ['price', 'is_available']
    search_fields = ['title']
    list_per_page = 20

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px; border-radius:6px;">', obj.image.url)
        return "—"
    thumbnail.short_description = "Image"


# ---------- Review ----------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['product__name', 'user__email']