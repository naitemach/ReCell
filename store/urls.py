from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchResults', views.search, name='searchResults'),
    path('catResults', views.catResults, name='catResults'),
    # path('orders', views.orders, name='orders'),
    path('sales', views.sales, name='sales'),
    path('login', views.login, name='login'),
    path('display', views.display, name='display'),
    path('productDetails', views.productDetails, name='productDetails'),
    path('register', views.register, name='register'),
    path('productReg', views.productReg, name='productReg'),
    path('productSummary',views.productSummary,name='productSummary'),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
