from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('home', views.home, name='home'),
    path('search', views.search, name='search'),
    path('login', views.login, name='login')
]
