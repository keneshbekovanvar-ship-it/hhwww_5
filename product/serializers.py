from rest_framework import serializers
from users.models import CustomUser
from .models import Product, ConfirmationCode
import random


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'birthdate', 'phone_number']

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            birthdate=validated_data.get('birthdate'),
            phone_number=validated_data.get('phone_number'),
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()

        code = str(random.randint(100000, 999999))

        ConfirmationCode.objects.create(
            user=user,
            code=code
        )

        print("CONFIRM CODE:", code)

        return user


class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            confirm = ConfirmationCode.objects.get(user=user)

            if confirm.code != data['code']:
                raise serializers.ValidationError("Неверный код")

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        return data

    def save(self):
        user = CustomUser.objects.get(email=self.validated_data['email'])
        user.is_active = True
        user.save()

        ConfirmationCode.objects.filter(user=user).delete()
        return user
