from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Prefetch, Q
from .models import *

def index(request):
    offer = OfferProduct.objects.filter(is_available=True)
    category = Category.objects.annotate(sub_count=Count('subcategory')).\
        prefetch_related(Prefetch('subcategory_set',
                                  queryset=SubCategory.objects.annotate(product_count=Count('product'))))

    sub_id = request.GET.get("subcategory")
    min_price = request.GET.get("min")
    max_price = request.GET.get("max")

    product = Product.objects.all()

    if sub_id:
        product = product.filter(subcategory=sub_id)

    if min_price and max_price:
        product = product.filter(price__range=(min_price, max_price))

    # Pagination — 12 products per page
    paginator = Paginator(product, 6)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "offer": offer,
        "category": category,
        "product": page_obj,   # now a Page object, still loops like a normal queryset
        "page_obj": page_obj,  # gives access to has_next, has_previous, etc.
    }
    if request.headers.get("HX-Request"):
        return render(request, "core/product.html", context)
    return render(request, "core/index.html", context)


def product_detail(request,id):
    product=get_object_or_404(Product,id=id)
    context={
        "product":product
    }
    return render(request,"core/product_detail.html", context)