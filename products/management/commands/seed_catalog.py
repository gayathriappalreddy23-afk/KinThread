from django.core.management.base import BaseCommand
from products.models import Brand, Category, Product


class Command(BaseCommand):
    help = 'Seed the catalog with sample categories, brands, and products for the homepage.'

    def handle(self, *args, **options):
        categories = [
            {'name': 'Men', 'slug': 'men'},
            {'name': 'Women', 'slug': 'women'},
            {'name': 'Accessories', 'slug': 'accessories'},
            {'name': 'Kids', 'slug': 'kids'},
            {'name': 'Beauty', 'slug': 'beauty'},
        ]

        brands = [
            {'name': 'Zara', 'slug': 'zara'},
            {'name': 'Nike', 'slug': 'nike'},
            {'name': 'Gucci', 'slug': 'gucci'},
        ]

        for data in categories:
            Category.objects.get_or_create(slug=data['slug'], defaults={'name': data['name']})

        for data in brands:
            Brand.objects.get_or_create(slug=data['slug'], defaults={'name': data['name']})

        products = [
            {
                'title': 'Classic White Tee',
                'slug': 'classic-white-tee',
                'description': 'A clean, versatile tee for everyday dressing.',
                'price': '29.99',
                'discount_price': '24.99',
                'category_slug': 'men',
                'brand_slug': 'zara',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=400&q=80',
                'is_trending': True,
                'is_new_arrival': False,
            },
            {
                'title': 'Urban Denim Jacket',
                'slug': 'urban-denim-jacket',
                'description': 'A modern denim jacket with a relaxed fit.',
                'price': '89.99',
                'discount_price': '79.99',
                'category_slug': 'men',
                'brand_slug': 'zara',
                'image_url': 'https://images.unsplash.com/photo-1495105787522-5334e3ffa0ebd?auto=format&fit=crop&w=400&q=80',
                'is_trending': False,
                'is_new_arrival': True,
            },
            {
                'title': 'Running Shoes',
                'slug': 'running-shoes',
                'description': 'Lightweight sneakers built for comfort.',
                'price': '120.00',
                'discount_price': '109.99',
                'category_slug': 'men',
                'brand_slug': 'nike',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=400&q=80',
                'is_trending': True,
                'is_new_arrival': False,
            },
            {
                'title': 'Tailored Formal Blazer',
                'slug': 'tailored-formal-blazer',
                'description': 'Sharp single-breasted suit jacket in wool blend.',
                'price': '149.99',
                'discount_price': '129.99',
                'category_slug': 'men',
                'brand_slug': 'gucci',
                'image_url': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=400&q=80',
                'is_trending': True,
                'is_new_arrival': True,
            },
            {
                'title': 'Floral Summer Dress',
                'slug': 'floral-summer-dress',
                'description': 'Bright florals for sunny days and brunch.',
                'price': '59.99',
                'discount_price': '49.99',
                'category_slug': 'women',
                'brand_slug': 'zara',
                'image_url': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=400&q=80',
                'is_trending': True,
                'is_new_arrival': False,
            },
            {
                'title': 'Elegant Evening Gown',
                'slug': 'elegant-evening-gown',
                'description': 'A glamorous gown for evening occasions.',
                'price': '299.99',
                'discount_price': '249.99',
                'category_slug': 'women',
                'brand_slug': 'gucci',
                'image_url': 'https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?auto=format&fit=crop&w=400&q=80',
                'is_trending': False,
                'is_new_arrival': True,
            },
            {
                'title': 'Casual Crop Top',
                'slug': 'casual-crop-top',
                'description': 'Soft and stylish for casual outfits.',
                'price': '24.99',
                'discount_price': '19.99',
                'category_slug': 'women',
                'brand_slug': 'zara',
                'image_url': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=400&q=80',
                'is_trending': True,
                'is_new_arrival': False,
            },
            {
                'title': 'Leather Tote Handbag',
                'slug': 'leather-tote-handbag',
                'description': 'Premium grain leather handbag with spacious compartments.',
                'price': '135.00',
                'discount_price': '119.99',
                'category_slug': 'accessories',
                'brand_slug': 'gucci',
                'image_url': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=400&q=80',
                'is_trending': True,
                'is_new_arrival': True,
            },
            {
                'title': 'Polarized Aviator Sunglasses',
                'slug': 'polarized-aviator-sunglasses',
                'description': 'Classic metal frame sunglasses with UV400 protection.',
                'price': '45.00',
                'discount_price': '35.00',
                'category_slug': 'accessories',
                'brand_slug': 'zara',
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=400&q=80',
                'is_trending': True,
                'is_new_arrival': False,
            },
            {
                'title': 'Kids Play Outfit',
                'slug': 'kids-play-outfit',
                'description': 'Comfortable essentials for active kids.',
                'price': '34.99',
                'discount_price': '29.99',
                'category_slug': 'kids',
                'brand_slug': 'nike',
                'image_url': 'https://images.unsplash.com/photo-1519238263530-99abca9665ae?auto=format&fit=crop&w=400&q=80',
                'is_trending': False,
                'is_new_arrival': True,
            },
            {
                'title': 'Luxury Perfume',
                'slug': 'luxury-perfume',
                'description': 'A signature fragrance for everyday elegance.',
                'price': '150.00',
                'discount_price': '129.99',
                'category_slug': 'beauty',
                'brand_slug': 'gucci',
                'image_url': 'https://images.unsplash.com/photo-1528701800487-ba01fea498c0?auto=format&fit=crop&w=400&q=80',
                'is_trending': True,
                'is_new_arrival': True,
            },
        ]

        for data in products:
            category = Category.objects.get(slug=data['category_slug'])
            brand = Brand.objects.get(slug=data['brand_slug'])
            Product.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'description': data['description'],
                    'price': data['price'],
                    'discount_price': data['discount_price'],
                    'category': category,
                    'brand': brand,
                    'image_url': data['image_url'],
                    'stock': 10,
                    'is_trending': data['is_trending'],
                    'is_new_arrival': data['is_new_arrival'],
                },
            )

        self.stdout.write(self.style.SUCCESS('Catalog seed completed successfully.'))
