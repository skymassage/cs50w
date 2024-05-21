from django.urls import path
from . import views

# We have a few routes named "index" throughout our different apps, 
# so declare a variable named "app_name" (necessary) to prevent Django getting confused.
app_name = "tasks" 

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add")
]