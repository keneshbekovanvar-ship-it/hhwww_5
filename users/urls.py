from django.urls import path
from .views import GoogleLoginView, GoogleCallbackView

urlpatterns = [
    path('google/login/', GoogleLoginView.as_view()),
    path('google/callback/', GoogleCallbackView.as_view()),
]
