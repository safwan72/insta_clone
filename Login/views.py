from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from . import forms, models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.

def login_index(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Main:home'))
            messages.success(request, 'Logged in Successfully')
        else:
            messages.warning(request, 'Log In Failed. Check Proper Inputs')
            return HttpResponseRedirect(reverse('App_Login:login'))    
    return render(request, "Login/Login.html",context={'form': form,'username_class': 'form-control',})


def sign_index(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save()
            # user.email=form.cleaned_data.get('email')
            # user.username=form.cleaned_data.get('username')
            # user.password=form.cleaned_data.get('password1')
            # user.save()
            messages.success(request, 'Account Created Successfully')
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, "Login/Signup.html",context={'form': form,'username_class': 'form-control',})


def myprofile(request):
    
    return render(request, "Profile/Profile.html",context={})
