from django.urls import path
from .views import register,login_view,product_list,add_to_cart,Cart_Item,create_order

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('product_list/', product_list, name='product_list'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('quantity/', Cart_Item, name='quantity'),
    path('create_order/', create_order, name='create_order'),
]
