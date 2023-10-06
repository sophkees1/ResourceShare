from typing import Optional
from django.contrib.auth import authenticate

from rest_framework.views import APIView # turn our class to API view
from rest_framework.response import Response # return JSON
from rest_framework import status # set status code
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token # generate token
from . import models
from . import serializers


class UserLogin(APIView):
    def post(self, request):
        # get credentials
        password = request.data.get("password")
        username = request.data.get("username")
        
        # Authenticate the user
        user: Optional[models.User] = authenticate(
            username = username,
            password = password,
        )
        if not user:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_404_NOT_FOUND
            )
        # create the token
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key},
            status=status.HTTP_201_CREATED
        )
        

class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = models.User.objects.prefetch_related("resources_set").get(
            id=request.user.id
        )
        response = serializers.UserProfileModelSerializer(user)
        return Response(response.data)