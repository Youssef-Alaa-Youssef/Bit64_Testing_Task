from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product,CartItem,Cart,Order

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    cart= CartSerializer()

    class Meta:
        model = CartItem
        fields = ['cart','product', 'quantity']

    def get_product(self, obj):
        product = obj.product
        return {
            'name': product.name,
            'price': product.price
        }
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'created_at']