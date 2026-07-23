from django.test import TestCase
from django.urls import reverse
from products.models import Category, Product, Brand
from .models import ContactMessage


class CategoryViewsTests(TestCase):
    def setUp(self):
        self.men_cat = Category.objects.create(name='Men', slug='men')
        self.women_cat = Category.objects.create(name='Women', slug='women')
        self.acc_cat = Category.objects.create(name='Accessories', slug='accessories')
        self.brand = Brand.objects.create(name='Zara', slug='zara')

        self.men_product = Product.objects.create(
            title='Men Suit Blazer',
            slug='men-suit-blazer',
            description='Tailored blazer for men',
            price='120.00',
            category=self.men_cat,
            brand=self.brand,
            stock=10,
        )
        self.women_product = Product.objects.create(
            title='Women Silk Dress',
            slug='women-silk-dress',
            description='Elegant silk dress',
            price='85.00',
            category=self.women_cat,
            brand=self.brand,
            stock=10,
        )
        self.acc_product = Product.objects.create(
            title='Leather Sunglasses Case',
            slug='leather-sunglasses-case',
            description='Handcrafted leather case',
            price='30.00',
            category=self.acc_cat,
            brand=self.brand,
            stock=10,
        )

    def test_men_view_renders_database_products(self):
        response = self.client.get(reverse('men'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Men Suit Blazer')
        self.assertContains(response, f"/cart/add/{self.men_product.id}/")

    def test_women_view_renders_database_products(self):
        response = self.client.get(reverse('women'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Women Silk Dress')
        self.assertContains(response, f"/cart/add/{self.women_product.id}/")

    def test_accessories_view_renders_database_products(self):
        response = self.client.get(reverse('accessories'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Leather Sunglasses Case')
        self.assertContains(response, f"/cart/add/{self.acc_product.id}/")

    def test_men_view_search_and_price_filtering(self):
        response = self.client.get(reverse('men'), {'q': 'blazer', 'min_price': '100'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Men Suit Blazer')

        response_filtered_out = self.client.get(reverse('men'), {'max_price': '50'})
        self.assertEqual(response_filtered_out.status_code, 200)
        self.assertNotContains(response_filtered_out, 'Men Suit Blazer')


class ContactPageTests(TestCase):
    def test_contact_form_saves_message_to_database(self):
        response = self.client.post(
            reverse('contact'),
            {
                'name': 'Alice Johnson',
                'email': 'alice@example.com',
                'subject': 'Hello KinThread',
                'message': 'I would like to learn more about your collections.',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='alice@example.com').exists())

