from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.login_index,name='login'),
    path("signup/", views.sign_index,name='signup'),
]
