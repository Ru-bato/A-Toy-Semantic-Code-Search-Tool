from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import register_user, login_user, FavoriteViewSet, SearchRecordViewSet

router = DefaultRouter()
router.register(r'favorites', FavoriteViewSet)  # 添加 FavoriteViewSet 路由
router.register(r'search_records', SearchRecordViewSet)

urlpatterns = [
    path('login/', login_user, name='login_user'),
    path('register/', register_user, name='register_user'),
    path('', include(router.urls)),
]
