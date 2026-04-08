from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate

from users.tokens import get_tokens_for_user
from common.validators import validate_age_from_token  # 👈 ВАЖНО

from .models import Product
from .serializers import (
    ProductSerializer,
    RegisterSerializer,
    ConfirmSerializer
)
from .permissions import IsModerator


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class ConfirmView(generics.GenericAPIView):
    serializer_class = ConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Аккаунт подтверждён"})


class LoginView(generics.GenericAPIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user:
            if not user.is_active:
                return Response(
                    {"error": "Аккаунт не подтверждён"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(get_tokens_for_user(user))

        return Response(
            {"error": "Неверные данные"},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsModerator()]

        return []


    def create(self, request, *args, **kwargs):
        validate_age_from_token(request)
        return super().create(request, *args, **kwargs)
