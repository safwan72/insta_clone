from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Your Email Address", "class": "form-control"}
        ),
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Your Username", "class": "form-control"}
        ),
    )
    password1 = forms.CharField(
        required=True,
        label="Enter Your Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter Your Password", "class": "form-control"}
        ),
    )
    password2 = forms.CharField(
        required=True,
        label="Confirm Your Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Your Password", "class": "form-control"}
        ),
    )

    class Meta:
        model=models.User
        fields=('email','username','password1','password2')
        
        
        
        
class LoginForm(AuthenticationForm):
    # email=forms.EmailField(required=True,label='',widget=forms.TextInput(attrs={                'class': "form-control",
    #             'style': 'width: 400px;margin-bottom:25px',
    # 'placeholder':"Enter Your Email Address"}))
    username = forms.EmailField(
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Your Email",
                "autocomplete": "off",
                
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Your Password",
            }
        ),
    )