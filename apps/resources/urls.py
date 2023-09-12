from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("resources/<int:id>", views.resource_detail, name="resource-detail"),
    path("resources/post/", views.resource_post, name="resource-post")
]
