from django.shortcuts import render,redirect
from .models import CustomUser
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import SignupForm,LoginForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST,request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            
            role = request.POST.get('role')
            user.role = role

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
                    return HttpResponse('user is seller')
                else:
                    return HttpResponse('user is buyer')
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
            return HttpResponse("Access denied")
        return view_func(request, *args, **kwargs)
    return wrapper