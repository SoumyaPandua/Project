from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('vegetables', 'vegetables'),
        ('fruits', 'fruits'),
        ('groceryitems', 'groceryitems'),
        ('nonveg', 'nonveg'),
    ]
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    image = models.ImageField(upload_to='Images/', blank=True, null=True)
    discount = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.get_name_display()

# Abstract base class to avoid repetition of common fields
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Images/', blank=True, null=True)

    class Meta:
        abstract = True

    def adjust_stock(self, quantity):
        self.stock -= quantity
        self.save()

    def restock(self, quantity):
        self.stock += quantity
        self.save()

# Models for each category
class Vegetable(Product):
    class Meta:
        verbose_name = "Vegetable"
        verbose_name_plural = "Vegetables"

class Fruit(Product):
    class Meta:
        verbose_name = "Fruit"
        verbose_name_plural = "Fruits"

class GroceryItem(Product):
    class Meta:
        verbose_name = "Grocery Item"
        verbose_name_plural = "Grocery Items"

class NonVeg(Product):
    class Meta:
        verbose_name = "Non-Veg"
        verbose_name_plural = "Non-Veg"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def subtotal(self):
        return self.product.price * self.quantity
