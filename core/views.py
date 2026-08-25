from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from django.db.models import Count, Prefetch, Q, Avg
from django.views.decorators.cache import never_cache
from .models import *
from .forms import *



@never_cache
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

    # Top rated: only products with at least one review, so unreviewed
    # products (avg_rating=None) don't sort to the top.
    top_rated = Product.objects.annotate(avg_rating=Avg("reviews__rating")) \
        .filter(avg_rating__isnull=False) \
        .order_by("-avg_rating")[:3]

    context = {
        "offer": offer,
        "category": category,
        "product": page_obj,
        "page_obj": page_obj,
        "top_rated": top_rated,
    }
    if request.headers.get("HX-Request"):
        return render(request, "core/product.html", context)
    return render(request, "core/index.html", context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = product.reviews.all()
    existing = Review.objects.filter(user=request.user, product=product).first()
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', id=product.id)

    # average rating + total count in one query instead of two
    rating_stats = reviews.aggregate(avg_rating=Avg('rating'), total_reviews=Count('id'))
    avg_rating = round(rating_stats['avg_rating'] or 0)
    total_reviews = rating_stats['total_reviews']

    related_product = Product.objects.filter(category=product.category).exclude(id=product.id)

    
   
    context = {
        "product": product,
        "form": form,
        "reviews": reviews,
        "range": range(1, 6),
        "existing": existing,
        "avg_rating": avg_rating,
        "total_reviews": total_reviews,
        "related_product": related_product,
        
    }

    return render(request, "core/product_detail.html", context)