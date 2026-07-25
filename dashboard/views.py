from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Category, Product, Order

@login_required(login_url='/')
def dashboard_view(request):
    query = request.GET.get('q', '').strip()
    categories = Category.objects.all()
    trending_products = Product.objects.filter(is_trending=True)[:10]
    new_arrivals = Product.objects.filter(is_new_arrival=True)[:8]
    
    # Dynamic queries for top collection gallery showcase
    top_collection = Product.objects.all()[:24]
    recent_orders = Order.objects.all()[:4]
    
    search_results = []

    if query:
        search_results = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__name__icontains=query)
        ).distinct()[:50]

    context = {
        'categories': categories,
        'trending_products': trending_products,
        'new_arrivals': new_arrivals,
        'top_collection': top_collection,
        'recent_orders': recent_orders,
        'search_query': query,
        'search_results': search_results,
    }
    return render(request, 'home.html', context)
