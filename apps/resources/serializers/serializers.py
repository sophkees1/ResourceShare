from rest_framework import serializers
from apps.user.serializers import UserModelSerializer
from apps.resources import models


# naming convention: <model>Serializer


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cat = serializers.CharField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    bio = serializers.CharField()


class ResourceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    link = serializers.URLField()
    user_id = UserSerializer()
    cat_id = CategorySerializer()
    tags = TagSerializer(many=True)
    
#####################################################################################################################################
class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__" # special string to serialize ALL attributes of model


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"


class ResourceModelSerializer(serializers.ModelSerializer):  
    cat_id = CategoryModelSerializer()
    tags = TagModelSerializer(many=True)
    user_id = UserModelSerializer()
    class Meta:
        model = models.Resources
        fields = (
            "id",
            "title",
            "description",
            "link",
            "cat_id",
            "tags",
            "user_id"
        )

