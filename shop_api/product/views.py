from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, ConfirmSerializer


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
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                return Response({"error": "Аккаунт не подтверждён"}, status=400)
            return Response({"message": "Вы вошли в систему"})
        return Response({"error": "Неверные данные"}, status=400)