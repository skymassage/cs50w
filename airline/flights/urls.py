from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), # Note that it's normal to get an error at the root URL, because we haven't set it yet.
    path("<int:flight_id>", views.flight, name="flight"),
    path("<int:flight_id>/book", views.book, name="book")
]