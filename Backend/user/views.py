from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Favorite
from .serializers import FavoriteSerializer


@api_view(['POST'])
def register_user(request):
    print(request.data)
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Although they will be checked at the frontend, they're possibly None for some reason.
    # For better robustness, do it again.
    if not username or not email or not password:
        print(1)
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if email already exists
    if User.objects.filter(email=email).exists():
        print(2)
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    # Create new user
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = True  # 确保用户被激活
        user.save()
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    print("success")
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    print(request.data)
    email = request.data.get('email')
    password = request.data.get('password')

    # Although they will be checked at the frontend, they're possibly None for some reason.
    # For better robustness, do it again.
    if not email or not password:
        return Response({'error': 'Email and Password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Use authenticate function
    user = authenticate(username=email, password=password)
    if user is not None:
        # Login success
        print(666)
        return Response({'message': 'Login successful', 'username': user.username}, status=status.HTTP_200_OK)

    else:
        print(999)
        return Response({'error': 'Email or Password error'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    serializer = FavoriteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # relate current user to favorite
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)
