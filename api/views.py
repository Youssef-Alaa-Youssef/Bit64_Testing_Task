from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

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
