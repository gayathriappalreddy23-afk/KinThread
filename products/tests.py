from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from .models import Category, Product, Brand


class CategoryPageTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Men', slug='men')
        self.accessories_category = Category.objects.create(name='Accessories', slug='accessories')
        self.brand = Brand.objects.create(name='Nike', slug='nike')
        Product.objects.create(
            title='Classic Tee',
            slug='classic-tee',
            description='A simple tee',
            price='29.99',
            category=self.category,
            brand=self.brand,
            stock=5,
        )
        Product.objects.create(
            title='Leather Bag',
            slug='leather-bag',
            description='A stylish bag',
            price='89.99',
            category=self.accessories_category,
            brand=self.brand,
            stock=4,
        )

    def test_seed_catalog_data_creates_homepage_content(self):
        call_command('seed_catalog')

        self.assertTrue(Category.objects.filter(slug='men').exists())
        self.assertTrue(Product.objects.filter(is_trending=True).exists())
        self.assertTrue(Product.objects.filter(is_new_arrival=True).exists())

    def test_category_page_renders_products(self):
        response = self.client.get(reverse('category-page', args=['men']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Classic Tee')

    def test_search_products_filters_by_query(self):
        response = self.client.get(reverse('search-products'), {'q': 'classic'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Classic Tee')

    def test_search_products_filters_by_category_slug(self):
        response = self.client.get(reverse('search-products'), {'q': 'bag', 'category_slug': 'accessories'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Leather Bag')
