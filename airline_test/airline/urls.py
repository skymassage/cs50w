"""
URL configuration for airline project.

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
from django.urls import include, path

# In order to use the admin app, we need to create an administrative account inside of our Django web application. 
# The way to do that is via the command line. Run "python manage.py create superuser", and set username, email address and password.
# And Django will create a superuser account in this web application so that we, using these credentials, 
# have the ability to visit the web interface for the admin app and actually manipulate some of these underlying models.
urlpatterns = [
    path('admin/', admin.site.urls),    # "/admin" takes us to the admin app, and you can log in to get Django's site administration interface.
    path("flights/", include("flights.urls")),
]
