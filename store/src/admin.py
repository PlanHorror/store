from django.contrib import admin
from .models import Profile, Product, Cart, Order, Checkout
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Checkout)

# Register your models here.
