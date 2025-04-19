from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stock/', views.get_stock_data, name='get_stock_data'),
]
