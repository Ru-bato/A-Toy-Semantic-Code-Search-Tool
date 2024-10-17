from django.urls import path

from . import views

urlpatterns = [
    path('get_popular/', views.get_popular_code_examples, name='get_popular'),
]
