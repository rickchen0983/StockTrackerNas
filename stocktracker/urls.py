from django.contrib import admin
from django.urls import path
from stocks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock/', views.home, name='home'),  # 顯示首頁的路由
    path('api/stock_data/', views.get_stock_data, name='get_stock_data'),  # 提供股市數據的 API 路由
]
