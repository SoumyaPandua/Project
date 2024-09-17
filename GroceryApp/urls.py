"""
URL configuration for GroceryApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from authapp.views import *
from website.views import *
from adminpanel.views import *
from customerpanel.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name="register"),
    path('login/', login_view, name="login"),
    path('', website, name='website'),
    path('logout/', logout_view, name='logout'),
    path('forgot_password/', forgot_password, name="forgot_password"),
    path('admin-dashboard/', admin_dashboard, name='admin'),
    path('admin_profile/', admin_profile, name='admin_profile'),
    path('vegetables/', vegetables, name='vegetables'),
    path('fruits/', fruits, name='fruit'),
    path('groceryitems/', groceryitems, name='groceryitems'),
    path('nonveg/', nonveg, name='nonveg'),
    path('p_profile', p_profile, name='p_profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('address/', address, name='address'),
    path('cart/', cart, name='cart'),
    path('order/', order, name='order'),
    path('manage-address/', manage_address, name='manage_address'),
    path('add_to_cart/<int:product_id>/<str:category>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('update_admin_profile/', update_admin_profile, name='update_admin_profile'),
    path('delete_admin_profile/', delete_admin_profile, name='delete_admin_profile'),
    path('add_product', add_product, name='add_product'),
    path('edit_product/<str:category>/<int:id>/', edit_product, name='edit_product'),
    path('delete_product/<str:category>/<int:id>/', delete_product, name='delete_product'),
    path('add_customer/', add_customer, name='add_customer'),
    path('edit_customer/<int:customer_id>/', edit_customer, name='edit_customer'),
    path('delete_customer/<int:customer_id>/', delete_customer, name='delete_customer'),
    path('razorpay_payment/', razorpay_payment, name='razorpay_payment'),
    path('razorpay_webhook/', razorpay_webhook, name='razorpay_webhook'),
    path('all_orders/', all_orders, name="all_orders"),
    path('verify-payment/', verify_payment, name='verify_payment'),
    path('success/', success, name='success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.static import static