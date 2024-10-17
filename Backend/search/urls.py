from django.urls import path

from .views import integrated_search

urlpatterns = [
    path('integrated_search/', integrated_search, name='integrated_search'),
]
