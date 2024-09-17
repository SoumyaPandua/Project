from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)

@admin.register(Vegetable)
class VegetableModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'price', 'stock', 'category']

@admin.register(Fruit)
class FruitModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'price', 'stock', 'category']

@admin.register(GroceryItem)
class GroceryItemModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'price', 'stock', 'category']

@admin.register(NonVeg)
class NonVegModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'price', 'stock', 'category']

