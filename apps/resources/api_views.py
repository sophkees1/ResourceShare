from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Resources, Category, Tag
from . import mixins
from .serializers import serializers


# function based

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
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
    return Response(response.data, status=200)


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
# mixins.FilterOutAdminResourcesMixin
class ListResource(mixins.FilterByCategoryMixin, ListAPIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)
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
class ResourceViewSets(mixins.FilterOutAdminResourcesMixin, viewsets.ModelViewSet):
    queryset = (
        Resources.objects.select_related("user_id", "cat_id")
        .prefetch_related("tags")
        .all()
    )
    serializer_class = serializers.ResourceModelSerializer
    
    
# always inherit mixin first
class CategoryViewSets(mixins.DenyDeletionOfDefaultCategoryMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryModelSerializer
    
    
class DeleteCategory(mixins.DenyDeletionOfDefaultCategoryMixin, DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryModelSerializer