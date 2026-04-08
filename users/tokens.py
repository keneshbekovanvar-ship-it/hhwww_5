from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)


    refresh['birthdate'] = str(user.birthdate) if user.birthdate else None

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
