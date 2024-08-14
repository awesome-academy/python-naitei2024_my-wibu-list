
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.forms import UserCreationForm

def homepage(request):
    return render(request, 'html/homepage.html')
 
 #Xử lý logic đăng ký, đăng nhập.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Thay thế 'login' bằng tên URL đăng nhập của bạn
    else:
        form = RegistrationForm()
    return render(request, 'html/registerform.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('homepage')  # Thay thế 'home' bằng tên URL bạn muốn chuyển hướng đến
    else:
        form = LoginForm()
    return render(request, 'html/loginform.html', {'form': form})
