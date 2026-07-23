from django.shortcuts import get_object_or_404, redirect, render
from products.models import Product


def _get_cart(request):
    cart = request.session.get('cart', [])
    if not isinstance(cart, list):
        cart = []
    return cart


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def cart_view(request):
    cart_items = _get_cart(request)
    products = []
    total = 0

    for item in cart_items:
        product = Product.objects.filter(pk=item.get('product_id')).first()
        if product:
            quantity = int(item.get('quantity', 1))
            subtotal = float(product.price) * quantity
            total += subtotal
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

    context = {
        'products': products,
        'total': total,
        'item_count': len(products),
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = _get_cart(request)
    found = False

    for item in cart:
        if item.get('product_id') == product_id:
            item['quantity'] = int(item.get('quantity', 1)) + 1
            found = True
            break

    if not found:
        cart.append({'product_id': product_id, 'quantity': 1})

    _save_cart(request, cart)
    return redirect('cart')
