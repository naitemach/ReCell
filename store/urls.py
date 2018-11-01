from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('home', views.home, name='home'),
    path('search', views.search, name='search'),
    path('login', views.login, name='login'),
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
