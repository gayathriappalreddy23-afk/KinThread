from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse


def google_login(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        if not email:
            messages.error(request, "Please enter an email address to continue.")
            return redirect(reverse('google_login'))

        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': email.split('@')[0].title(),
            },
        )
        if created:
            user.set_unusable_password()
            user.save()
        login(request, user)
        messages.success(request, "Signed in with Google")
        return redirect('dashboard')

    email = request.GET.get('email', '').strip().lower()
    if email:
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': email.split('@')[0].title(),
            },
        )
        if created:
            user.set_unusable_password()
            user.save()
        login(request, user)
        messages.success(request, "Signed in with Google")
        return redirect('dashboard')

    return render(request, 'google_login.html')


def google_callback(request):
    return redirect(reverse('google_login'))


def auth_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        first_name = (request.POST.get('first_name') or '').strip()
        last_name = (request.POST.get('last_name') or '').strip()
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''
        confirm_password = request.POST.get('confirm_password') or ''

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(f"{reverse('auth_home')}?form=signup")

        if User.objects.filter(Q(username__iexact=email) | Q(email__iexact=email)).exists():
            messages.error(request, "Already registered")
            return redirect(f"{reverse('auth_home')}?form=signup")

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        messages.success(request, "Signup successful. Please login.")
        return redirect(f"{reverse('auth_home')}?form=login")

    return redirect('auth_home')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('auth_home')


def login_view(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect(f"{reverse('auth_home')}?form=login")

    return redirect('auth_home')
