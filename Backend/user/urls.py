from django.urls import path

from .views import register_user, login_user, add_favorite, list_favorites

urlpatterns = [
    path('login/', login_user, name='login_user'),
    path('register/', register_user, name='register_user'),
    path('favorites/', add_favorite, name='add_favorite'),
    path('favorites/list/', list_favorites, name='list_favorites'),
]
