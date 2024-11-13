from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
# Create your models here.
# User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = True
User._meta.get_field('email').null = True
# Extend the User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    def __str__(self):
        return self.parent_name + "'s profile"
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    def __str__(self):
        return self.name
class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    # Set price = product.price * quantity when saving
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + "'s bill"
    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super(Bill, self).save(*args, **kwargs)
