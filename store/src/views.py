from django.shortcuts import render, redirect, get_object_or_404
from .form import SignUpForm, Profile_Form, SignInForm
from .models import Profile, Product, Cart, Checkout, Order
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
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
        if not request.user.is_authenticated:
            messages.error(request, 'Bạn cần đăng nhập để thêm vào giỏ hàng!')
            return redirect('/signin/')
        print('POST:', request.POST.get('addCart'))
        print('POST:', request.POST.get('buyNow'))
        if request.POST.get('addCart') is not None:
            print('Add to cart')
            # Current cart
            this_cart = Cart.objects.filter(user=request.user, product=product)
            if this_cart:
                this_cart = this_cart[0]
                this_cart.quantity += int(request.POST['quantity'])
                this_cart.save()
            else:
                product = Product.objects.get(pk=product_id)
                quantity = request.POST['quantity']
                cart = Cart(user=request.user, product=product, quantity=quantity)
                cart.save()
            quantity = Cart.objects.filter(user=request.user, product=product)[0].quantity
            messages.success(request, 'Thêm vào giỏ hàng thành công! số lượng: %s' % (quantity))
            return redirect('/product/%s-%s' % (slugify(product.name), product.id))
        if request.POST.get('buyNow') is not None:
            print('Buy now')
            messages.success(request, 'Đặt hàng thành công!')
            return redirect('/')
        # return redirect('/checkout/%s-%s-%s' % (slugify(product.name), product.id, request.POST['quantity']))
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
@login_required(login_url='/signin/')
def cart(request):
    cart = Cart.objects.filter(user=request.user)
    # Calculate total price for each product in cart
    for item in cart:
        if item.product.sale_price == 0:
            item.total_price = item.product.price * item.quantity
        else:
            item.total_price = item.product.sale_price * item.quantity
    if request.method == 'POST':
        print('POST:', request.POST)
        # Change quantity of each product in cart
        for item in cart:
            item.quantity = request.POST['quantity_%s' % (item.product.id)]
            item.save()
        return redirect('/checkout')
    return render(request, 'src/cart.html', {'cart': cart})
@login_required(login_url='/signin/')
def delete_cart(request, cart_id):
    cart = Cart.objects.get(pk=cart_id)
    cart.delete()
    messages.success(request, 'Xóa sản phẩm khỏi giỏ hàng thành công!')
    # return redirect('/cart')
    return redirect(request.META['HTTP_REFERER'])
@login_required(login_url='/signin/')
def checkout(request):
    cart = Cart.objects.filter(user=request.user)
    # Calculate total price for each product in cart
    total_price = 0
    total_product = 0
    for item in cart:
        if item.product.sale_price == 0:
            item.total_price = item.product.price * item.quantity
        else:
            item.total_price = item.product.sale_price * item.quantity
        total_price += item.total_price
        total_product += 1
    if total_product == 0:
        messages.error(request, 'Giỏ hàng của bạn trống!')
        return redirect('/cart')
    if request.method == 'POST':
        print('POST:', request.POST)
        # Validate phone number
        if not request.POST['phone_number'].isdigit():
            messages.error(request, 'Số điện thoại không hợp lệ!')
            return redirect(request.META['HTTP_REFERER'])
        if len(request.POST['phone_number']) < 8 or len(request.POST['phone_number']) > 12:
            messages.error(request, 'Số điện thoại không hợp lệ!')
            return redirect(request.META['HTTP_REFERER'])
        # Create checkout
        checkout = Checkout(user=request.user, full_name=request.POST['name'], payment_method=request.POST['payment'], address=request.POST['address'], phone_number=request.POST['phone_number'], notes=request.POST['notes'], product_count=total_product, total_price=total_price)
        checkout.save()
        # Create order
        for item in cart:
            order = Order(user=request.user, product=item.product, quantity=item.quantity, total_price=item.total_price, checkout=checkout)
            order.save()
            # Delete cart
            item.delete()
        messages.success(request, 'Đặt hàng thành công!')
        return redirect('/')
    return render(request, 'src/checkout.html', {'cart': cart, 'total_price': total_price, 'total_product': total_product})
