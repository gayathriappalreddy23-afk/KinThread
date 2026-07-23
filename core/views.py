from django.shortcuts import render
from django.db.models import Q
from products.models import Category, Product, Brand
from .models import ContactMessage


def _get_category_context(request, slug, default_title, default_intro, accent):
    category, _ = Category.objects.get_or_create(slug=slug, defaults={'name': default_title.split('’')[0]})
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
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    brands = Brand.objects.filter(products__category=category).distinct()

    return {
        'category': category,
        'products': products,
        'brands': brands,
        'query': query,
        'brand': brand,
        'min_price': min_price,
        'max_price': max_price,
        'page_title': default_title,
        'page_intro': default_intro,
        'accent': accent,
    }


def about_view(request):
    return render(request, 'about.html')


def men_view(request):
    context = _get_category_context(
        request,
        'men',
        'Men’s World',
        'Explore our fashion collection for men with premium fabrics and tailored fits.',
        '#1f2937'
    )
    return render(request, 'men.html', context)


def women_view(request):
    context = _get_category_context(
        request,
        'women',
        'Women’s World',
        'Discover trendy outfits curated just for you.',
        '#c2185b'
    )
    return render(request, 'women.html', context)


def accessories_view(request):
    context = _get_category_context(
        request,
        'accessories',
        'Accessories Collection',
        'Upgrade your style with the latest accessories.',
        '#2e7d32'
    )
    return render(request, 'accessories.html', context)


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and subject and message:
            ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)

        return render(request, 'contact.html', {'submitted': True})

    return render(request, 'contact.html', {'submitted': False})

