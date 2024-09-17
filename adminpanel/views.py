from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from website.models import *
from authapp.models import *
from django.contrib.auth import logout
from django.core.paginator import Paginator


def admin_dashboard(request):
    total_admins = User.objects.filter(role='admin').count()
    total_customers = User.objects.filter(role='customer').count()
    total_items = (
        Vegetable.objects.count() +
        Fruit.objects.count() +
        GroceryItem.objects.count() +
        NonVeg.objects.count()
    )
    
    context = {
        'total_admins': total_admins,
        'total_customers': total_customers,
        'total_items': total_items,
        'profile_image': request.user.profile_image.url if request.user.profile_image else None
    }
    return render(request, 'admin.html', context)


User = get_user_model()

@login_required
def admin_profile(request):
    user = request.user
    context = {
        'full_name': user.full_name,
        'email': user.email,
    }
    return render(request, 'a_profile.html', context)


@login_required
def update_admin_profile(request):
    user = request.user
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        profile_image = request.FILES.get('profile_image')

        user.full_name = full_name
        user.email = email
        if profile_image:
            user.profile_image = profile_image
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('admin_profile')
    
    return render(request, 'a_profile.html', {'user': user})

@login_required
def delete_admin_profile(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Profile deleted successfully!')
        logout(request)
        return redirect('http://127.0.0.1:8000/')
    return render(request, 'a_profile.html', {'user': user})

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('productname')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category = request.POST.get('category')
        image = request.FILES.get('file')

        if category == 'vegetables':
            Vegetable.objects.create(name=product_name, price=price, stock=stock, category_id=1, image=image)
        elif category == 'fruit':
            Fruit.objects.create(name=product_name, price=price, stock=stock, category_id=2, image=image)
        elif category == 'groceryitems':
            GroceryItem.objects.create(name=product_name, price=price, stock=stock, category_id=3, image=image)
        elif category == 'nonveg':
            NonVeg.objects.create(name=product_name, price=price, stock=stock, category_id=4, image=image)
        
        return redirect('add_product')

    vegetables = Vegetable.objects.all()
    fruits = Fruit.objects.all()
    groceryitems = GroceryItem.objects.all()
    nonvegs = NonVeg.objects.all()

    context = {
        'vegetables': vegetables,
        'fruits': fruits,
        'groceryitems': groceryitems,
        'nonvegs': nonvegs,
    }
    return render(request, 'add_product.html', context)

def edit_product(request, category, id):
    if category == 'vegetables':
        product = get_object_or_404(Vegetable, id=id)
    elif category == 'fruit':
        product = get_object_or_404(Fruit, id=id)
    elif category == 'groceryitems':
        product = get_object_or_404(GroceryItem, id=id)
    elif category == 'nonveg':
        product = get_object_or_404(NonVeg, id=id)

    if request.method == 'POST':
        product.name = request.POST.get('productname')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.image = request.FILES.get('file')
        product.save()
        return redirect('add_product')

    context = {'product': product, 'category': category}
    return render(request, 'edit_product.html', context)

def delete_product(request, category, id):
    if category == 'vegetables':
        product = get_object_or_404(Vegetable, id=id)
    elif category == 'fruit':
        product = get_object_or_404(Fruit, id=id)
    elif category == 'groceryitems':
        product = get_object_or_404(GroceryItem, id=id)
    elif category == 'nonveg':
        product = get_object_or_404(NonVeg, id=id)

    product.delete()
    return redirect('add_product')




from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
import random
import string

def generate_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def add_customer(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        role = request.POST.get('role')

        # Validate and convert role
        role = 'admin' if role == '1' else 'customer'

        # Generate a password and create the user
        password = generate_password()
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            full_name=full_name,
            role=role
        )

        # Send email with login details
        send_mail(
            'Your New Account Details',
            f'Hello {full_name},\n\nYour account has been created.\nUsername: {email}\nPassword: {password}\n\nPlease change your password after logging in.\n\nBest regards,\nYour Team',
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )

        # Redirect after creating user
        return redirect('add_customer')

    # Pagination
    customers_list = User.objects.filter(role='customer').order_by('id')
    paginator = Paginator(customers_list, 3)  # Show 3 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "add_customer.html", {'page_obj': page_obj})



def edit_customer(request, customer_id):
    customer = get_object_or_404(User, id=customer_id, role='customer')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        # Update customer data
        customer.full_name = full_name
        customer.email = email
        customer.role = role
        customer.save()
        
        return redirect('add_customer')  # Redirect after update

    return render(request, "edit_customer.html", {'customer': customer})


def delete_customer(request, customer_id):
    customer = get_object_or_404(User, id=customer_id, role='customer')
    customer.delete()
    return redirect('add_customer')


from .models import Order

def all_orders(request):
    orders = Order.objects.select_related('user').order_by('-created_at')
    paginator = Paginator(orders, 7)  # Show 7 orders per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'all_orders.html', context)
