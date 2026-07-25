from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('update/<int:product_id>/<str:action>/', views.update_cart_quantity, name='update-cart-quantity'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('payment-success/', views.payment_success_view, name='payment_success'),
]

