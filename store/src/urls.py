from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),  
    path('product/<slug:product_name>-<int:product_id>', views.product, name='product'),
    path('product', views.products, name='products'),
    path('cart', views.cart, name='cart'),
    path('delete_cart/<int:cart_id>' , views.delete_cart, name='delete_cart'),
    path('checkout/', views.checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)