from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Here we aren't actually directed to this route, we just us JS in the template to show the URL changing
    # and we can also decide what URL to display using JS.
    path("sections/<int:num>", views.section, name="section")
]