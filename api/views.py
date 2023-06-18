from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Product,CartItem,Cart
from .serializers import ProductSerializer,CartItemSerializer,CartSerializer
from rest_framework.views import APIView
from rest_framework import generics, permissions

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
class UserRegistrationView(APIView):
    throttle_classes = [UserRateThrottle]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'message': 'User registered successfully'})
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

@api_view(['POST'])
@csrf_exempt
@throttle_classes([UserRateThrottle])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        return Response({'message': 'User logged in successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])
def product_list(request):
    queryset = Product.objects.all().order_by('price')

    search_query = request.query_params.get('search', None)
    if search_query is not None:
        queryset = queryset.filter(Q(name__icontains=search_query))

    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    if not product_id or not quantity:
        return Response({'message': 'Invalid request data.'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'message': 'Product not found.'}, status=404)

    if not request.user.is_authenticated:
        return Response({'message': 'User must be authenticated to add products to the cart.'}, status=401)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += int(quantity)
    cart_item.save()

    return Response({'message': 'Product added to the cart successfully.'}, status=201)

@api_view(['GET'])
def Cart_Item(request):
    queryset = CartItem.objects.all()
    serializer = CartItemSerializer(queryset, many=True)
    return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

@api_view(['POST'])
def create_order(request):
    cart = request.user.cart

    if not cart.products.exists():
        return Response({'message': 'Cart is empty.'}, status=400)

    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save(user=request.user, products=cart.products.all())
        cart.products.clear()  
        return Response({'message': 'Order created successfully.', 'order_id': order.id}, status=201)

    return Response(serializer.errors, status=400)



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def view_cart(request):
    cart = request.user.cart  
    cart_items = cart.cartitem_set.all()  # Assuming you have a ForeignKey relationship between Cart and CartItem models

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/view.html', context)


class CartView(APIView):
    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
    

