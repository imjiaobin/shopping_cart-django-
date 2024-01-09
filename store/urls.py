from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
        #Leave as empty string for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    
    path('update_item/',views.updateItem,name='update_item'),#登入者狀態更新購物車狀態觸發
    path('process_order/', views.processOrder, name="process_order"),
]