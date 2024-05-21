from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),   
    path("category", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create_listing", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("bid", views.bid, name="bid"),
    path("close", views.close, name="close"),
]
