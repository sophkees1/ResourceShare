from django.urls import path
from rest_framework import routers
from . import views
from . import api_views

# TODO: check difference between simplerouter and defaultrouter
router = (routers.SimpleRouter())
router.register("api/v3/resource", api_views.ResourceViewSets) # base url

api_urlpatterns = [
    path("api/v1/resource/", api_views.list_resources, name="list-resources"),
    path("api/v1/categories/", api_views.list_category, name="list-categories"),
    path("api/v1/tags/", api_views.list_tags, name="list-tags"),
    path("api/v2/resource/", api_views.ListResource.as_view(), name="list-resources-class"),
    path("api/v2/categories/", api_views.ListCategory.as_view(), name="list-category-class"),
    path("api/v2/resource/<int:id>/", api_views.DetailResource.as_view(), name="detail-resource-class"),
]

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("resources/<int:id>", views.resource_detail, name="resource-detail"),
    path("resources/post/", views.resource_post, name="resource-post"),
    *api_urlpatterns,
    *router.urls,
]
