
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
    path("edit", views.edit, name="edit"),
    path("comment", views.comment, name="comment"),
    path("show_comment/<int:post_id>", views.show_comment, name="show_comment"),
    path("rate", views.rate, name="rate")
]
