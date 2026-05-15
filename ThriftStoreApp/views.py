from django.shortcuts import render,redirect,get_object_or_404
from .models import CustomUser,ProductDb,CategoryDb,CartDb
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import SignupForm,LoginForm,AddProductForm
from django.contrib.auth.decorators import login_required

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
        quantity = request.POST.get('quantity')
        total_price = request.POST.get('total_price')

        CartDb.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )
        return redirect('home_page')

    return render(request,'buyer/product_page.html',{'product': product})