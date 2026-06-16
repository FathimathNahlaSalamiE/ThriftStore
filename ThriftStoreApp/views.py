from django.shortcuts import render,redirect,get_object_or_404
from .models import CustomUser,ProductDb,CategoryDb,CartDb,AddressDb,OrderDb,OrderItem
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import SignupForm,LoginForm,AddProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST,request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            
            role = request.POST.get('role')

            if role == 'seller':
                user.role = 'seller'
            else:
                user.role = 'buyer'

            user.save()

            return redirect('login')
    else:
        form = SignupForm()
    
    return render(request,'signup.html',{'form':form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username,password=password)

            if user is not None:
                login(request,user)

                if user.role == 'seller':
                    return redirect('seller_products')
                else:
                    return redirect('home_page')
            else:
                return render(request,'login.html',{'form':form,'error':'Invalid credentials'})        
    else:
        form = LoginForm()

    return render(request,'login.html',{'form':form})



def logout_view(request):
    logout(request)
    return redirect('login')



def seller_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'seller':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper



@login_required
@seller_required
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST,request.FILES)
    
        if form.is_valid():
            product = form.save(commit=False)
            product.product_seller = request.user
            product.save()

            return redirect('seller_products')
    else:
        form = AddProductForm()

    return render(request,'seller/add_product.html',{'form':form})


@login_required
@seller_required
def seller_products(request):
    product_list = ProductDb.objects.filter(product_seller= request.user)
    ProductDb.objects.filter(product_image='').delete()
    return render(request,'seller/seller_products.html',{'product_list':product_list})


@login_required
@seller_required
def edit_product(request,id):
    product = get_object_or_404(
        ProductDb,
        id= id,
        product_seller = request.user
    )

    if request.method == "POST":
        form = AddProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_products')
    else:
        form = AddProductForm(instance=product)
    
    return render(request,'seller/edit_product.html',{'form':form})


@login_required
@seller_required
def delete_product(request,id):
    product = get_object_or_404(
        ProductDb,
        id=id,
        product_seller= request.user
    )

    product.delete()
    return redirect('seller_products')



@login_required
def home_page(request):
    product_list = ProductDb.objects.all()
    category_list = CategoryDb.objects.all()
    return render(request,'buyer/home_page.html',{'product_list':product_list,'category_list':category_list})



@login_required
def display_products(request,category_name):
    product_list = ProductDb.objects.filter(product_category__category_name=category_name)
    return render(request,'buyer/display_products.html',{'product_list':product_list})


@login_required
def view_product(request,id):
    product = ProductDb.objects.get(id = id)
    return render(request,'buyer/view_product.html',{'product':product})



@login_required
def add_to_cart(request,id):
    product = ProductDb.objects.get(id=id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))

        price = product.product_price
        total_price = quantity*price

        CartDb.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            price=price,
            total_price=total_price
        )

        return redirect('cart_page')

    return render(request,'buyer/view_product.html',{'product': product})

@login_required
def cart_page(request):
    cart_items = CartDb.objects.filter(user=request.user)

    total_amount = 0
    for item in cart_items:
        total_amount += item.total_price

    return render(request, 'buyer/cart_page.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

@login_required
def increase_quantity(request, id):
    item = CartDb.objects.get(id=id)

    item.quantity += 1
    item.total_price = item.quantity * item.price
    item.save()

    return redirect('cart_page')

@login_required
def decrease_quantity(request, id):
    item = CartDb.objects.get(id=id)

    if item.quantity > 1:
        item.quantity -= 1
        item.total_price = item.quantity * item.price
        item.save()

    return redirect('cart_page')

@login_required
def delete_cart(request, id):
    cart_item = CartDb.objects.get(id=id)
    cart_item.delete()
    
    return redirect('cart_page')


@login_required
def checkout(request):
    cart_items = CartDb.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart_page')

    total_amount = sum(item.total_price for item in cart_items)

    return render(request, 'buyer/checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

@login_required
def address_page(request):
    if request.method == "POST":
        print("Address form submitted")
        AddressDb.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            house_name=request.POST.get('house_name'),
            street=request.POST.get('street'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode')
        )
        print("Redirecting to payment page")
        return redirect('payment_page')

    return render(request, 'buyer/address.html')

@login_required
def payment_page(request):

    cart_items = CartDb.objects.filter(user=request.user)

    total = sum(item.total_price for item in cart_items)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Thrift Store Order',
                    },
                    'unit_amount': int(total * 100),
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='http://127.0.0.1:8000/ThriftStoreApp/payment_success/',
        cancel_url='http://127.0.0.1:8000/ThriftStoreApp/payment_cancel/',
    )

    return redirect(checkout_session.url)


@login_required
def payment_success(request):

    cart_items = CartDb.objects.filter(user=request.user)

    total = sum(item.total_price for item in cart_items)

    order = OrderDb.objects.create(
        user=request.user,
        total_amount=total,
        payment_status='Paid'
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.price,
            total_price=item.total_price
        )

    cart_items.delete()

    return render(request, 'buyer/success.html')

@login_required
def payment_cancel(request):
    return render(request, 'buyer/payment_cancel.html')

@login_required
def my_orders(request):

    orders = OrderDb.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request,'buyer/my_orders.html',{'orders': orders})

@login_required
def order_again(request, id):

    order_item = get_object_or_404(
        OrderItem,
        id=id,
        order__user=request.user
    )

    cart_item, created = CartDb.objects.get_or_create(
        user=request.user,
        product=order_item.product,
        defaults={
            'quantity': order_item.quantity,
            'price': order_item.price,
            'total_price': order_item.total_price
        }
    )

    if not created:
        cart_item.quantity += order_item.quantity
        cart_item.total_price = (
            cart_item.quantity * cart_item.price
        )
        cart_item.save()

    return redirect('cart_page')