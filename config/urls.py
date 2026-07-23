"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from core.views import about_view, contact_view, men_view, women_view, accessories_view
from dashboard.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('home/', dashboard_view, name='home'),
    path('dashboard/', include('dashboard.urls')),
    path('men/', men_view, name='men'),
    path('women/', women_view, name='women'),
    path('accessories/', accessories_view, name='accessories'),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
]
