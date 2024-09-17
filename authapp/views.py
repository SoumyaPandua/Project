from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
import re
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[@#$]", password):
        return False
    return True

def register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']
        
        User = get_user_model()
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect('register')
        
        if not is_valid_password(password1):
            messages.error(request, "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
            return redirect('register')

        try:
            user = User(
                username=email,
                email=email,
                full_name=full_name,
                role=role
            )
            user.set_password(password1)
            user.save()

            # Send email
            subject = 'Welcome to Our Website!'
            message = f'Hi {full_name},\n\nThank you for registering at our website.\n\nBest regards,\nYour Website Team'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('register')

    return render(request, 'register.html')




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.role == role:
                login(request, user)
                request.session['user_role'] = user.role
                print(user.role)
                messages.success(request, "Login successful!")
                return redirect('http://127.0.0.1:8000/')
            else:
                messages.error(request, "Invalid role. Please try again.")
                return redirect('login')
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "forgot_password.html")
        
        try:
            user = User.objects.get(email=email)
            user.password = make_password(password1)
            user.save()

            # Send email notification
            subject = 'Password Updated Successfully'
            message = (
                f'Hello {user.full_name},\n\n'
                f'Your password has been updated successfully. Please log in with your new password.\n\n'
                f'Thank you.'
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            messages.success(request, "Password updated successfully.")
            return redirect('login')  # Redirect to login page

        except User.DoesNotExist:
            messages.error(request, "Email address not found.")
            return render(request, "forgot_password.html")
    
    return render(request, "forgot_password.html")