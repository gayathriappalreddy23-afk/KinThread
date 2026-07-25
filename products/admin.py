from django.contrib import admin
from .models import Category, Brand, Product, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'brand', 'stock', 'is_trending', 'is_new_arrival']
    list_filter = ['category', 'brand', 'is_trending', 'is_new_arrival']
    list_editable = ['price', 'is_trending', 'is_new_arrival', 'stock']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'items_badges', 'total_amount', 'created_at']
    list_filter = ['created_at']
