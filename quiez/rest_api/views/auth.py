from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_auth.views import UserDetailsView as RestAuthUserDetailsView

from django.contrib.auth.models import User

from quiez.rest_api.serializers.auth import UserSerializer


class UserRegistrationView(GenericAPIView):
    """
    User registration view.
    """
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        """
        Registration function for new users.
        * Email will be used as username.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            str_username = serializer.validated_data["email"]
            serializer.validated_data["username"] = str_username
            try:
                user = User.objects.get(username=str_username)
                return Response({'detail': 'User with given email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                User.objects.create_user(**serializer.validated_data)
                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(RestAuthUserDetailsView):
    """
    User details view.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """
        Reads the user's details.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
