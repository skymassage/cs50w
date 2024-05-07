
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("profile/<str:username>", views.profile, name="profile"),

    # API routes
    path("comment/<int:post_id>", views.comment, name="comment"),
    path("edit", views.edit, name="edit"),
]
