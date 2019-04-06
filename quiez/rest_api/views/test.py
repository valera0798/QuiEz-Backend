from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..serializers.test import TestPostSerializer, TestGetSerializer
from ..models.test import Test


class TestList(GenericAPIView):
    """
    Test view class.

    post:
    Create test instance.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = TestPostSerializer

    def post(self, request):
        """
        Creates test instance using passed JSON from request body.

        :param request: test creation initiator.
        :return: HTTP response with id of created test instance.
        """
        serializer = TestPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            test = serializer.create(validated_data=serializer.validated_data)
            return Response({"test_id": test.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestDetail(GenericAPIView):
    """
    Test view class.

    get:
    Read test instance by id.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TestGetSerializer

    def get(self, request, test_id: int):
        """
        Reads test instance by id.

        :param request: test read initiator.
        :param test_id: test instance id.
        :return: HTTP response with serialized test instance.
        """
        test = get_object_or_404(Test, pk=test_id)
        serializer = TestGetSerializer(test)
        return Response(serializer.data, status=status.HTTP_200_OK)
