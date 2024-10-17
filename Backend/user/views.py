from django.contrib.auth import authenticate
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Favorite, SearchRecord
from .serializers import FavoriteSerializer, SearchRecordSerializer


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
    email = request.data.get('email')
    password = request.data.get('password')

    # Although they will be checked at the frontend, they're possibly None for some reason.
    # For better robustness, do it again.
    if not email or not password:
        return Response({'error': 'Email and Password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Use authenticate function
    user = authenticate(username=email, password=password)
    if user is not None:
        # 创建 token
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Favorite.objects.all()  # 定义 queryset

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)  # 仅返回当前用户的收藏

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # 关联当前用户

    def destroy(self, request, *args, **kwargs):
        title = kwargs.get('pk')
        try:
            favorite = self.get_queryset().get(item_title=title)  # 根据 title 查找
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SearchRecordViewSet(viewsets.ModelViewSet):
    queryset = SearchRecord.objects.all()
    serializer_class = SearchRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)