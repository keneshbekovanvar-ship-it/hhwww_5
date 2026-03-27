from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ConfirmationCode
import random

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            is_active=False  # ❗ НЕАКТИВНЫЙ
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
    username = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            confirm = ConfirmationCode.objects.get(user=user)

            if confirm.code != data['code']:
                raise serializers.ValidationError("Неверный код")

        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        return data

    def save(self):
        user = User.objects.get(username=self.validated_data['username'])
        user.is_active = True
        user.save()

        ConfirmationCode.objects.filter(user=user).delete()
        return user