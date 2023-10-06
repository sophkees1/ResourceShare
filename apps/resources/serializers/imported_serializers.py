from rest_framework import serializers
from apps.resources import models


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
    
    class Meta:
        model = models.Resources
        fields = (
            "id",
            "title",
            "description",
            "link",
            "cat_id",
            "tags",
        )

