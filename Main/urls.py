from django.urls import path, include
from . import views

app_name='App_Main'

urlpatterns = [
    path("", views.home_index,name='home'),
    path("explore/", views.explore_view,name='explore'),
]
