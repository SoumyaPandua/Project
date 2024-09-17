from django.shortcuts import render
from .models import *

def website(request):
    user_role = request.session.get('user_role')
    categories = Category.objects.all()
    return render(request, 'website.html', {'user_role': user_role, 'categories': categories})

def vegetables(request):
    all_vegetables = Vegetable.objects.all()
    return render(request, 'vegetables.html', {'vegetables': all_vegetables})

def fruits(request):
    all_fruits = Fruit.objects.all()
    return render(request, 'fruits.html', {'fruits': all_fruits})

def groceryitems(request):
    all_groceryitems = GroceryItem.objects.all()
    return render(request, 'groceryitems.html', {'groceryitems': all_groceryitems})

def nonveg(request):
    all_nonvegs = NonVeg.objects.all()
    return render(request, 'nonveg.html', {'nonvegs': all_nonvegs})


from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Vegetable, Fruit, GroceryItem, NonVeg

@login_required
def add_to_cart(request, product_id, category):
    content_type = ContentType.objects.get_for_model(Vegetable) if category == 'vegetables' else \
                   ContentType.objects.get_for_model(Fruit) if category == 'fruits' else \
                   ContentType.objects.get_for_model(GroceryItem) if category == 'groceryitems' else \
                   ContentType.objects.get_for_model(NonVeg) if category == 'nonveg' else \
                   None
    
    if content_type is None:
        return redirect('website')  # Or handle as needed
    
    product = get_object_or_404(content_type.model_class(), id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, content_type=content_type, object_id=product_id)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


from django.shortcuts import redirect, get_object_or_404
from .models import Cart, CartItem

def remove_from_cart(request, item_id):
    # Get the cart for the logged-in user
    cart = get_object_or_404(Cart, user=request.user)
    # Get the item to remove
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    # Redirect back to the cart
    return redirect('cart')



from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Vegetable, Fruit, GroceryItem, NonVeg

@require_POST
def update_cart_item(request, item_id):
    try:
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)
        
        # Get the cart for the logged-in user
        cart = get_object_or_404(Cart, user=request.user)
        
        # Get the item to update
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        # Get the product
        product = item.product
        
        # Adjust stock based on new quantity
        if quantity > item.quantity:
            product.adjust_stock(quantity - item.quantity)
        else:
            product.restock(item.quantity - quantity)
        
        # Update item quantity
        item.quantity = quantity
        item.save()
        
        # Update subtotal and total
        cart.total_price = sum(item.subtotal() for item in cart.items.all())
        cart.save()
        
        return JsonResponse({'status': 'success', 'total_price': cart.total_price})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
