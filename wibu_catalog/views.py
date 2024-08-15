from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm

def homepage(request):
    return render(request, 'html/homepage.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('homepage')
    else:
        form = RegistrationForm()
    return render(request, 'html/registerform.html', {'form': form})
