from django.contrib import admin
from .models import Category, Brand, Product

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
    list_display = ['title', 'price', 'category', 'is_trending', 'is_new_arrival', 'stock']
    list_filter = ['category', 'brand', 'is_trending', 'is_new_arrival']
    list_editable = ['price', 'is_trending', 'is_new_arrival', 'stock']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
