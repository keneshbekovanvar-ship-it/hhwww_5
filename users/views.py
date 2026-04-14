import requests
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now

from .models import CustomUser
from .tokens import get_tokens_for_user


class GoogleLoginView(APIView):
    def get(self, request):
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            "?response_type=code"
            f"&client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
            "&scope=openid email profile"
        )
        return redirect(google_auth_url)


class GoogleCallbackView(APIView):
    def get(self, request):
        code = request.GET.get('code')

        token_url = "https://oauth2.googleapis.com/token"

        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_response = requests.post(token_url, data=data)
        token_json = token_response.json()

        access_token = token_json.get("access_token")

        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        user_info = requests.get(
            user_info_url,
            params={"access_token": access_token}
        ).json()

        email = user_info.get("email")
        first_name = user_info.get("given_name")
        last_name = user_info.get("family_name")

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "is_active": True,
            }
        )

        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.last_login = now()
        user.save()

        tokens = get_tokens_for_user(user)

        return Response(tokens)
