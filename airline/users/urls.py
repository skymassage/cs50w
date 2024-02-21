from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]
# We have gone to the admin site (/admin) and added some users as the following:
# Username: harry
# Password: helloharry
# First name: Harry
# Last name: Potter
# Email address: harrypotter@example.com
# -------------------------------------------------
# Username: ron
# Password: helloron
# First name: Ron
# Last name: Weasley
# Email address: ronweasley@example.com