from django.shortcuts import render, redirect, get_object_or_404
from .form import SignUpForm, Profile_Form, SignInForm
from .models import Profile, Product, Bill
from django.contrib.auth import login, authenticate
from django.contrib import messages, auth
from django.conf import settings
from django.utils.text import slugify
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    products = list(Product.objects.all())
    # Take product by list of product id
    list_id = [1, 2, 3, 4]
    products = Product.objects.filter(id__in=list_id)
    # Print slug name of the first product
    # print('Slug name:', slugify(product.name))
    # Make money format with comma after every 3 digits
    for product in products:
        product.price = "{:,}".format(product.price)
        product.sale_price = "{:,}".format(product.sale_price)
    return render(request, 'src/home.html', {'products': products})
def signup(request):
    if request.user.is_authenticated:
        messages.error(request, 'Bạn đã đăng nhập!')
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = Profile_Form(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Tạo tài khoản thành công!')
            return redirect('/')
        else:
            messages.error(request, 'Tạo tài khoản không thành công!')
            print(form.errors)
    else:
        form = SignUpForm()
        profile_form = Profile_Form()
    return render(request, 'src/signup.html', {'form': form, 'profile_form': profile_form})
def signin(request):
    if request.user.is_authenticated:
        messages.error(request, 'Bạn đã đăng nhập!')
        return redirect('/')
    signin_form = SignInForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Đăng nhập thành công!')
            return redirect('/')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    return render(request, 'src/signin.html', {'signin_form': signin_form})
def signout(request):
    auth.logout(request)
    return redirect('/')
def product(request, product_id, product_name):
    product = get_object_or_404(Product, pk=product_id)
    # Make money format with comma after every 3 digits
    product.price = "{:,}".format(product.price)
    product.sale_price = "{:,}".format(product.sale_price)
    # Take list of product_uses
    product.product_uses = product.product_uses.split(';')
    if request.method == 'POST':
        print('POST:', request.POST)
        redirect('product', product_id=product_id, product_name=product_name)
    return render(request, 'src/product.html', {'product': product})
def products(request):
    products = list(Product.objects.all())
    # Make money format with comma after every 3 digits
    for product in products:
        product.price = "{:,}".format(product.price)
        product.sale_price = "{:,}".format(product.sale_price)
    # Pagination with 9 products per page
    paginator = Paginator(products, 9)
    page = request.GET.get('page',1)
    products = paginator.get_page(page)
    print('Products:', products)
    return render(request, 'src/products.html', {'products': products})
def test(request):
    products = list(Product.objects.all())
    # Make money format with comma after every 3 digits
    for product in products:
        product.price = "{:,}".format(product.price)
        product.sale_price = "{:,}".format(product.sale_price)
    # Pagination with 9 products per page
    paginator = Paginator(products, 9)
    page = request.GET.get('page',1)
    products = paginator.get_page(page)
    print('Products:', products)
    return render(request, 'src/test.html', {'products': products})
    