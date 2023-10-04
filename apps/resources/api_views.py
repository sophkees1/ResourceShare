from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import viewsets
from .models import Resources, Category, Tag
from . import serializers


# function based
@api_view(['GET'])
def list_resources(request):
    queryset = (
        Resources.objects.select_related("user_id", "cat_id")
        .prefetch_related("tags")
        .all()
    )
    
    response = serializers.ResourceModelSerializer(queryset, many=True)
    # transform to JSON before returning
    return Response(response.data)


@api_view(['GET'])
def list_category(request):
    queryset = Category.objects.all()

    response = serializers.CategoryModelSerializer(queryset, many=True)
    return Response(response.data)


@api_view(['GET'])
def list_tags(request):
    queryset = Tag.objects.all()
    
    response = serializers.TagModelSerializer(queryset, many=True)
    return Response(response.data)



### WITHOUT SERIALIZERS ###
    # response = [
    #     {
    #         "title": query.title,
    #         "link": query.link,
    #         "user": {
    #             "id": query.user_id.id, 
    #             "username": query.user_id.username
    #         },
    #         "category": query.cat_id.cat,
    #         "tags": query.all_tags(),
    #     }
    #     for query in queryset
    # ]
    
### CLASS BASED
class ListResource(ListAPIView):
    queryset = (
        Resources.objects.select_related("user_id", "cat_id")
        .prefetch_related("tags")
        .all()
    )
    serializer_class = serializers.ResourceModelSerializer
    
    
class ListCategory(ListAPIView):
    queryset = Category.objects.all()
    
    serializer_class = serializers.CategoryModelSerializer
    
    
class DetailResource(RetrieveAPIView):
    lookup_field = "id" # by default this is pk
    queryset = (
        Resources.objects.select_related("user_id", "cat_id")
        .prefetch_related("tags")
        .all()
    )
    serializer_class = serializers.ResourceModelSerializer
    
# ViewSets permits us to perform the CRUD operations in one class based view
# name convention <model>ViewSets
class ResourceViewSets(viewsets.ModelViewSet):
    queryset = (
        Resources.objects.select_related("user_id", "cat_id")
        .prefetch_related("tags")
        .all()
    )
    serializer_class = serializers.ResourceModelSerializer