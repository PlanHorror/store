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
    path('test/', views.test, name='test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)