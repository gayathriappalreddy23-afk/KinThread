from django.test import TestCase
from django.urls import reverse
from products.models import Category, Product


class CartViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Men', slug='men')
        self.product = Product.objects.create(
            title='Classic Oxford Shirt',
            slug='classic-oxford-shirt',
            description='Oxford shirt for men',
            price='45.00',
            category=self.category,
            stock=10,
        )

    def test_add_to_cart_adds_item_to_session_and_redirects(self):
        response = self.client.get(reverse('add-to-cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('cart'))

        cart = self.client.session.get('cart')
        self.assertIsNotNone(cart)
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart[0]['product_id'], self.product.id)
        self.assertEqual(cart[0]['quantity'], 1)

    def test_cart_view_displays_added_products_and_total(self):
        self.client.get(reverse('add-to-cart', args=[self.product.id]))
        self.client.get(reverse('add-to-cart', args=[self.product.id]))

        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Classic Oxford Shirt')
        self.assertContains(response, 'Qty: 2')
        self.assertContains(response, 'Total: $90.0')

