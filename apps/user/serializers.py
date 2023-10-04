from rest_framework import serializers
from . import models

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        # to show all fields EXCEPT: use exclude()-- must be a tuple 
        exclude = ("password",)
        
# class UserUpdateModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.User
#         fields = ("username", "password")