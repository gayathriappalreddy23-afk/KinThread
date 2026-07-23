from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_view, name='auth_home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('google-login/', views.google_login, name='google_login'),
    path('google-callback/', views.google_callback, name='google_callback'),
]
