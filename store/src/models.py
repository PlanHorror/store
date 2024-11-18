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
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + "'s profile"
class Product(models.Model):
    name = models.CharField(max_length=100)
    objects_used = models.TextField( default='')
    description = models.TextField( default='')
    product_uses = models.TextField( default='')
    price = models.IntegerField()
    sale_price = models.IntegerField()
    image1 = models.ImageField(upload_to='products/', default='products/default.jpg')
    image2 = models.ImageField(upload_to='products/', default='products/default.jpg')
    image3 = models.ImageField(upload_to='products/', default='products/default.jpg')
    image4 = models.ImageField(upload_to='products/', default= 'products/default.jpg')
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + "'s cart"
class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, choices=(('COD', 'Thanh toán khi nhận hàng'), ('MOMO', 'Thanh toán qua MOMO'), ('VISA', 'Thanh toán qua VISA')))
    address = models.TextField()
    # Phone regex using format 8 - 12 digits and can have +84 or 0 at the beginning
    phone_number = models.CharField( max_length=17)
    notes = models.TextField(blank=True, null=True)
    product_count = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.IntegerField()
    status = models.CharField(max_length=100, default='Pending', choices=(('Pending', 'Xác thực đơn hàng'), ('Delivering', 'Đang vận chuyển'), ('Delivered', 'Đã vận chuyển')))
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + "'s checkout" + ' - ' + str(self.created_at.strftime('%d/%m/%Y %H:%M:%S'))
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.IntegerField()
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + "'s order"
    def save(self, *args, **kwargs):
        self.total_price = self.product.sale_price * self.quantity
        super(Order, self).save(*args, **kwargs)