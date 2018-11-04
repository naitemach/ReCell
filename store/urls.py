from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('searchResults', views.search, name='searchResults'),
    re_path(r'^catResults/$', views.catResults, name='catResults'),
    path('catResults', views.catResults, name='catResults'),
    path('orders', views.orders, name='orders'),
    path('sales', views.sales, name='sales'),
    path('login', views.login, name='login'),
    path('display', views.display, name='display'),
    re_path(r'^productDetails/$', views.productDetails, name='productDetails'),
    path('productDetails', views.productDetails, name='productDetails'),
    path('register', views.register, name='register'),
    path('productReg', views.productReg, name='productReg'),
    path('cart',views.cart, name='cart'),
    path('search',views.search, name='search'),

    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
