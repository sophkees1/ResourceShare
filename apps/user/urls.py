from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.user_list, name="user-list"),
    path("login/", views.login_view, name="login-view"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_view, name="logout-view"),
    #path("update/<int:id>", views.UpdateUser.as_view(), name="update-user")
]
