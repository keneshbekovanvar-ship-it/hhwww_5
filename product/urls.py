from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/categories/', CategoryListCreateView.as_view()),
    path('api/v1/categories/<int:pk>/', CategoryDetailView.as_view()),

    path('api/v1/products/', ProductListCreateView.as_view()),
    path('api/v1/products/<int:pk>/', ProductDetailView.as_view()),

    path('api/v1/reviews/', ReviewListCreateView.as_view()),
    path('api/v1/reviews/<int:pk>/', ReviewDetailView.as_view()),
]
