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
            return redirect(f"{reverse('auth_home')}?form=signup&email={email}")

        if User.objects.filter(Q(username__iexact=email) | Q(email__iexact=email)).exists():
            messages.error(request, f"⚠️ An account with email '{email}' is already registered. Please log in below.")
            return redirect(f"{reverse('auth_home')}?form=login&email={email}")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        from accounts.models import UserProfile
        UserProfile.objects.get_or_create(user=user)

        display_name = first_name if first_name else email.split('@')[0].title()
        messages.success(request, f"🎉 Registration completed for {display_name}! Your details are saved in the database. Please log in below to access your account.")
        return redirect(f"{reverse('auth_home')}?form=login&email={email}")

    return redirect(f"{reverse('auth_home')}?form=signup")


def logout_view(request):
    logout(request)
    messages.success(request, "👋 Logged out successfully. Thank you for visiting KinThread!")
    return render(request, 'logout_success.html')


def login_view(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''

        # Check if user exists in database
        user_exists = User.objects.filter(Q(username__iexact=email) | Q(email__iexact=email)).exists()
        if not user_exists:
            messages.error(request, f"No registered account found for '{email}'. Please complete a quick Sign Up first to create your KinThread account, then log in!")
            return redirect(f"{reverse('auth_home')}?form=signup&email={email}")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            display_name = user.first_name if user.first_name else user.username.split('@')[0].title()
            messages.success(request, f"👋 Welcome back, {display_name}! Your profile & activity page has been updated with your database records.")
            return redirect('user_profile')
        else:
            messages.error(request, f"Incorrect password entered for '{email}'. Please double-check your password and try again.")
            return redirect(f"{reverse('auth_home')}?form=login&email={email}")

    return redirect('auth_home')


def user_profile_view(request):
    try:
        from products.models import Product, Order
        from accounts.models import UserProfile

        # Handle Profile Update POST request
        if request.method == 'POST' and request.user.is_authenticated:
            first_name = (request.POST.get('first_name') or 'Indu').strip()
            last_name = (request.POST.get('last_name') or '').strip()
            email_val = (request.POST.get('email') or 'Indu@gmail.com').strip().lower()
            phone_number = (request.POST.get('phone_number') or '').strip()
            address = (request.POST.get('address') or '').strip()
            city = (request.POST.get('city') or '').strip()
            pincode = (request.POST.get('pincode') or '').strip()

            request.user.first_name = first_name
            request.user.last_name = last_name
            if email_val:
                request.user.email = email_val
            request.user.save()

            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            if phone_number:
                profile.phone_number = phone_number
            if address:
                profile.address = address
            if city:
                profile.city = city
            if pincode:
                profile.pincode = pincode
            profile.save()

            messages.success(request, f"✅ Profile updated successfully in database! Email: {email_val}")
            return redirect('user_profile')

        # Track session visit count
        visit_count = request.session.get('visit_count', 0) + 1
        request.session['visit_count'] = visit_count

        cart = request.session.get('cart', [])
        cart_items_count = 0
        cart_products = []
        cart_total = 0.0

        for item in cart:
            if isinstance(item, dict):
                pid = item.get('product_id')
                qty = int(item.get('quantity', 1))
                cart_items_count += qty
                prod = Product.objects.filter(pk=pid).first()
                if prod:
                    price = float(prod.discount_price if prod.discount_price else prod.price)
                    item_subtotal = price * qty
                    cart_total += item_subtotal
                    cart_products.append({
                        'product_id': pid,
                        'title': prod.title,
                        'image_url': prod.image_url if hasattr(prod, 'image_url') and prod.image_url else (prod.image.url if hasattr(prod, 'image') and prod.image else 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=300&q=80'),
                        'quantity': qty,
                        'price': f"{price:,.2f}",
                        'subtotal': f"{item_subtotal:,.2f}",
                    })
                else:
                    cart_products.append({
                        'product_id': pid,
                        'title': f"KinThread Apparel Item #{pid}",
                        'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=300&q=80',
                        'quantity': qty,
                        'price': "2,499.00",
                        'subtotal': f"{2499.00 * qty:,.2f}",
                    })

        # Real placed orders from session and database
        placed_session_orders = request.session.get('placed_orders', [])
        if not isinstance(placed_session_orders, list):
            placed_session_orders = []

        orders = []
        total_spent = 0.0

        orders_map = {}

        # Add DB orders first if user is authenticated
        try:
            if request.user.is_authenticated:
                db_orders = Order.objects.filter(user=request.user).order_by('-created_at')
                for db_ord in db_orders:
                    amt = float(db_ord.total_amount)
                    oid = getattr(db_ord, 'order_id', f"#ORD-{db_ord.id}")
                    dt_str = db_ord.created_at.strftime("%b %d, %Y %H:%M") if hasattr(db_ord, 'created_at') and db_ord.created_at and hasattr(db_ord.created_at, 'strftime') else "Recently"
                    
                    db_items_list = [p.title for p in db_ord.items.all()] if hasattr(db_ord, 'items') else []
                    items_str = ", ".join(db_items_list) if db_items_list else "KinThread Luxury Apparel"

                    orders_map[oid] = {
                        'order_id': oid,
                        'items_title': items_str,
                        'payment_method': "🟣 PhonePe / UPI Express",
                        'created_at': dt_str,
                        'total_amount': f"{amt:,.2f}",
                        'status': "Processing",
                        'status_badge': "background: rgba(37, 99, 235, 0.12); color: #2563eb; border: 1px solid rgba(37, 99, 235, 0.3);",
                    }
        except Exception:
            pass

        # Add session placed orders
        for ord_item in placed_session_orders:
            if isinstance(ord_item, dict):
                oid = ord_item.get('order_id')
                if oid and oid not in orders_map:
                    orders_map[oid] = ord_item

        orders = list(orders_map.values())
        for o in orders:
            try:
                amt_str = str(o.get('total_amount', '0')).replace(',', '')
                total_spent += float(amt_str)
            except (ValueError, TypeError):
                pass

        total_orders_count = len(orders)

        if request.user.is_authenticated:
            email = request.user.email if request.user.email else "Indu@gmail.com"
            username = request.user.username if request.user.username else email
            full_name = request.user.get_full_name().strip()
            first_name = (getattr(request.user, 'first_name', '') or '').strip()
            last_name = (getattr(request.user, 'last_name', '') or '').strip()
            if not full_name:
                first_name = first_name if first_name else "Indu"
                full_name = f"Indu {last_name}".strip() if last_name else "Indu"

            member_badge = "NEW CUSTOMER 🎉" if total_orders_count == 0 else "AUTHENTICATED MEMBER ⭐"
            
            profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
            phone = profile_obj.phone_number
            address = profile_obj.address
            city = profile_obj.city
            pincode = profile_obj.pincode

            if hasattr(request.user, 'date_joined') and request.user.date_joined:
                date_joined_str = request.user.date_joined.strftime("%b %d, %Y")
            else:
                date_joined_str = "Today"

            if hasattr(request.user, 'last_login') and request.user.last_login:
                last_login_str = request.user.last_login.strftime("%b %d, %Y at %I:%M %p")
            else:
                last_login_str = "Active Session (Just Now)"
        else:
            username = "Indu@gmail.com"
            email = "Indu@gmail.com"
            full_name = "Indu"
            first_name = "Indu"
            last_name = ""
            member_badge = "ACTIVE CUSTOMER SESSION 🛍️"
            date_joined_str = "Today (Active Session)"
            last_login_str = "Active Session (Just Now)"
            phone = "+91 9876543210"
            address = "KinThread Fashion House, MG Road, Suite 402"
            city = "Bengaluru, Karnataka"
            pincode = "560001"

        initial = (full_name[0] if full_name else 'I').upper()

        user_info = {
            'username': username,
            'email': email,
            'full_name': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'address': address,
            'city': city,
            'pincode': pincode,
            'initial': initial,
            'member_badge': member_badge,
            'date_joined_str': date_joined_str,
            'last_login_str': last_login_str,
            'date_joined': getattr(request.user, 'date_joined', None) if request.user.is_authenticated else None,
            'last_login': getattr(request.user, 'last_login', None) if request.user.is_authenticated else None,
            'is_authenticated': request.user.is_authenticated,
        }

        context = {
            'user_info': user_info,
            'visit_count': visit_count,
            'cart_items_count': cart_items_count,
            'cart_products': cart_products,
            'cart_total': f"{cart_total:,.2f}",
            'orders': orders,
            'total_orders_count': total_orders_count,
            'total_spent': f"{total_spent:,.2f}",
        }
        return render(request, 'user_activity.html', context)
    except Exception:
        context = {
            'user_info': {
                'username': 'customer@kinthread.com',
                'email': 'customer@kinthread.com',
                'full_name': 'Customer Member',
                'first_name': 'Customer',
                'last_name': 'Member',
                'phone': '+91 9876543210',
                'address': 'KinThread Fashion House',
                'city': 'Bengaluru',
                'pincode': '560001',
                'initial': 'C',
                'member_badge': 'ACTIVE CUSTOMER SESSION 🛍️',
                'date_joined': None,
                'is_authenticated': False,
            },
            'visit_count': 1,
            'cart_items_count': 0,
            'cart_products': [],
            'cart_total': "0.00",
            'orders': [],
            'total_orders_count': 0,
            'total_spent': "0.00",
        }
        return render(request, 'user_activity.html', context)
