from django.shortcuts import render

# Create your views here.

def login_index(request):
    return render(request, "Login/PreLogin.html")


def sign_index(request):
    return render(request, "Login/Login.html")
