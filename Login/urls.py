from django.urls import path, include
from . import views

app_name='App_Login'

urlpatterns = [
    path("login/", views.login_index,name='login'),
    path("signup/", views.sign_index,name='signup'),
    path("logout/", views.logout_user,name='logout'),
    path("profile/<id>/", views.myprofile,name='profile'),
    path('follow/<id>',views.follow,name='follow'),
    path('unfollow/<id>',views.unfollow,name='unfollow'),
]
