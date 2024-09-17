from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .models import Address
from .razorpay_utils import client
from website.models import Cart

User = get_user_model()

@login_required
def p_profile(request):
    user = request.user
    context = {
        'full_name': user.full_name,
        'email': user.email,
    }
    return render(request, 'p_profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
      full_name = request.POST.get('full_name')
      user = request.user
      user.full_name = full_name
      user.save()
      send_mail(
        'Profile Updated',
        'Dear {},\n\nYour profile has been successfully updated.'.format(user.get_full_name()),
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
      )
      messages.success(request, 'Profile updated successfully!')
      return redirect('p_profile')
    else:
        return redirect('p_profile')

@login_required
def delete_profile(request):
    user = request.user
    user_email = user.email  # Store email before deletion
    user_full_name = user.get_full_name()  # Store full name before deletion
    user.delete()

    # Send delete email
    send_mail(
        'Profile Deleted',
        'Dear {},\n\nYour profile has been successfully deleted. We are sorry to see you go.'.format(user_full_name),
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

    messages.success(request, 'Your account has been deleted successfully!')
    return redirect('http://127.0.0.1:8000/')

def address(request):
    return redirect('manage_address')


@login_required
def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'cart.html', {'cart': cart})

def order(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'orders.html', {'orders': orders})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Address

@login_required
def manage_address(request):
    user = request.user
    addresses = Address.objects.filter(user=user).order_by('-id')  # Order by latest address
    cart = Cart.objects.get(user=user)

    if addresses.exists():
        address = addresses.first()  # Get the latest address
        is_update = True
    else:
        address = None
        is_update = False

    if request.method == 'POST':
        if 'update' in request.POST and is_update:
            address.first_name = request.POST['first_name']
            address.last_name = request.POST['last_name']
            address.address = request.POST['address']
            address.landmark = request.POST['landmark']
            address.email = request.POST['email']
            address.phone = request.POST['phone']
            address.additional_info = request.POST['additional_info']
            address.save()
            return redirect('manage_address')  # Replace 'manage_address' with your address page URL name
        elif 'add' in request.POST and not is_update:
            Address.objects.create(
                user=user,
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                address=request.POST['address'],
                landmark=request.POST['landmark'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                additional_info=request.POST['additional_info']
            )
            return redirect('manage_address')  # Replace 'manage_address' with your address page URL name

    context = {
        'form': address,
        'is_update': is_update,
        'cart_total': cart.total_price,
    }
    return render(request, 'address.html', context)


import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

import uuid
from django.shortcuts import redirect
from adminpanel.models import *

@login_required
def razorpay_payment(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    amount = int(cart.total_price() * 100)

    addresses = Address.objects.filter(user=user).order_by('-id')
    if addresses.exists():
        address = addresses.first()
        phone = address.phone
    else:
        phone = ''

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

    razorpay_order_id = payment['id']
    order_id = str(uuid.uuid4())[:8]
    Order.objects.create(
        user=user,
        order_id=order_id,
        razorpay_order_id=razorpay_order_id,
        amount=amount / 100,
        total_items=cart.items.count(),
        status='pending'
    )

    context = {
        'amount': amount // 100,
        'api_key': settings.RAZORPAY_KEY_ID,
        'order_id': razorpay_order_id,
        'user': user,
        'email': user.email,
        'phone': phone,
    }
    return render(request, 'razorpay_payment.html', context)




@csrf_exempt
def razorpay_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        payment_id = data.get('payload', {}).get('payment', {}).get('entity', {}).get('id', '')
        order_id = data.get('payload', {}).get('payment', {}).get('entity', {}).get('order_id', '')
        status = data.get('payload', {}).get('payment', {}).get('entity', {}).get('status', '')

        try:
            order = Order.objects.get(order_id=order_id)
            if status == 'captured':
                order.status = 'completed'
                cart = Cart.objects.get(user=order.user)
                cart.items.all().delete()
            elif status == 'failed':
                order.status = 'failed'
            else:
                order.status = 'pending'

            order.save()
            return JsonResponse({"status": "ok"})
        except Order.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Order not found"}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import razorpay

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

        payment_id = data.get('payment_id')
        razorpay_order_id = data.get('order_id')
        signature = data.get('signature')

        if not all([payment_id, razorpay_order_id, signature]):
            return JsonResponse({"status": "error", "message": "Missing payment details"}, status=400)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            client.utility.verify_payment_signature(params_dict)

            try:
                order = Order.objects.get(razorpay_order_id=razorpay_order_id)
                order.status = 'completed'
                order.save()

                cart = Cart.objects.get(user=order.user)
                items = cart.items.all()
                cart.items.all().delete()

                # Debug: Check if items are retrieved
                print(f"Items in cart: {items}")

                # Prepare product details for email
                product_details = "\n".join(
                    [f"{item.product.name}: ₹{item.product.price} x {item.quantity}" for item in items if item.product and item.product.name and item.product.price]
                )
                if not product_details:
                    product_details = "No products found."

                total_price = order.amount

                # Prepare email body
                email_body = (
                    f"Thank you for your purchase!\n\n"
                    f"Order ID: {order.order_id}\n"
                    f"Products:\n{product_details}\n\n"
                    f"Total Price: ₹{total_price}\n\n"
                    f"Thank you for shopping with us!"
                )

                # Debug: Print email content
                print("Email body:", email_body)

                send_mail(
                    'Order Confirmation',
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [order.user.email],
                    fail_silently=False,
                )

                return JsonResponse({"status": "completed", "redirect_url": "/success/"})

            except Order.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Order not found"}, status=404)

        except razorpay.errors.SignatureVerificationError:
            try:
                order = Order.objects.get(razorpay_order_id=razorpay_order_id)
                order.status = 'failed'
                order.save()
            except Order.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Order not found"}, status=404)

            return JsonResponse({"status": "failed"})

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)



def success(request):
    return render(request, 'success.html')
