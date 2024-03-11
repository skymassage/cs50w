from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Even we aren't directed to this route, we still need this to address data from the "fetch()" JS function in the templates. 
    path("sections/<int:num>", views.section, name="section") 
]