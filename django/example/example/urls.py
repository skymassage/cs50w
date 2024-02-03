# urls.py contains directions for where users should be routed after navigating to a certain URL or what URLs I can access.
"""
URL configuration for example project.

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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # A path is already given to us by default called admin, it runs a default Django application called the admin application.

    # In this urls.py, we want to be able to include all of the paths from the urls.py within the application using
    # "include("<APP_NAME>.urls")", rather than adding a function from views.py to the second argument like we do in the urls.py of the application
    # Here means to tell Django to look at the urls.py inside of the "hello" directory to figure out what additional URLs I can get to from there. 
    # So this is one master urls.py file that might connect to multiple different other URL configurations that exist as well. 
    path('hello/', include("hello.urls"))
]
