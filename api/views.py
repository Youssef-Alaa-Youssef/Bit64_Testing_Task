from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Product,CartItem,Cart
from .serializers import ProductSerializer,CartItemSerializer

@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
