<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import RegistrationForm
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
            return redirect('homepage')  # Thay thế 'login' bằng tên URL đăng nhập của bạn
    else:
        form = RegistrationForm()
    return render(request, 'html/registerform.html', {'form': form})
>>>>>>> 815b201 (Create registration page)
