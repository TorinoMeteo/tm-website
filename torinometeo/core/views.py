from django.contrib.auth import authenticate

from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from core.serializers import UserSerializer


class LoginView(views.APIView):
    """
    API authentication.
    Checks if the provided credentials correspond to an user associated
    with an account, in such case the user token is returned in a
    200 response.
    """

    def post(self, request, format='json'):

        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                serialized = UserSerializer(user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': serialized.data
                })
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    """
    User unauthentication.
    If the requests arrives from an authenticated client performs a logout
    @TODO regenerate token
    """
    def post(self, request, format='json'):
        return Response({
            'status': 'OK',
            'message': 'Logout succedeed.'
        }, status=status.HTTP_200_OK)
