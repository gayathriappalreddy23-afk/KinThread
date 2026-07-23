from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .models import Brand, Category, Product


def category_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category).order_by('-created_at')

    query = request.GET.get('q', '').strip()
    brand = request.GET.get('brand', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(brand__name__icontains=query)
        )

    if brand:
        products = products.filter(brand__slug=brand)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    brands = Brand.objects.filter(products__category=category).distinct()

    context = {
        'category': category,
        'products': products,
        'brands': brands,
        'query': query,
        'brand': brand,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'category_page.html', context)


def search_products(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category_slug', '').strip()
    products = Product.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(brand__name__icontains=query)
        )

    context = {
        'products': products[:20],
        'query': query,
        'category_slug': category_slug,
    }
    return render(request, 'search_results.html', context)
