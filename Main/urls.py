from django.urls import path, include
from . import views

app_name='App_Main'

urlpatterns = [
    path("", views.home_index,name='home'),
    path("explore/", views.explore_view,name='explore'),
    path("add_post/", views.add_Post,name='add_post'),
    path("like/<id>/", views.liked,name='like'),
    path("unlike/<id>/", views.unliked,name='unlike'),
]
