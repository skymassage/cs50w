"""
URL configuration for django_example project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py contains directions for where users should be routed after navigating to a certain URL or what URLs I can access.
from django.contrib import admin
from django.urls import path, include

# "urlpatterns" is a list of all of the allowable URLs that can be accessed for the particular app.
urlpatterns = [
    path('admin/', admin.site.urls), # A path is already given to us by default called admin, it runs a default Django application called the admin application.

    # In this urls.py, we want to be able to include all of the paths from the urls.py within the application using
    # "include("<APP_NAME>.urls")", rather than adding a function from views.py to the second argument like we do in the urls.py of each app.
    # The first following line means to tell Django to look at the urls.py inside of the "hello" directory to figure out what additional URLs I can get to from there.
    # So this is one master urls.py file that might connect to multiple different other URL configurations that exist as well. 
    path('hello/', include("hello.urls")),
    path('newyear/', include("newyear.urls")),
    path('tasks/', include("tasks.urls"))
    # Because we don't set "path('', include("<APP_NAME>.urls"))" for the root URL, 
    # you will encounter the 404 page at the homepage (localhost:8000).
]
