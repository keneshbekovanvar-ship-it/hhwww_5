from django.urls import path
from .views import RegisterView, LoginView, ConfirmView

urlpatterns = [
    path('api/v1/users/register/', RegisterView.as_view()),
    path('api/v1/users/login/', LoginView.as_view()),
    path('api/v1/users/confirm/', ConfirmView.as_view()),
]
