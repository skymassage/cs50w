from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    # Django uses sessions and middleware to hook the authentication system into "request" objects.
    # These provide a "request.user" attribute and a "request.auser" async method on every request 
    # which represents the current user. If the current user has not logged in, 
    # this attribute will be set to an instance of AnonymousUser class, otherwise it will be an instance of User class.
    # You can tell them apart with ".is_authenticated".

    # Every actual User object always returns True for ".is_authenticated", but an AnonymousUser object will return False.
    # If the user logs out, then "request.user" will be the AnonymousUser instead of User, 
    # and "request.user.is_authenticated == False".

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Use "authenticate()" to verify a set of credentials. It takes credentials as keyword arguments, 
        # username and password for the default case, checks them against each authentication backend, 
        # and returns a User object if the credentials are valid for a backend. 
        # If the credentials aren't valid for any backend or if a backend raises PermissionDenied, it returns None. 
        # "request" is an optional HttpRequest which is passed on "authenticate()" of the authentication backends.
        user = authenticate(request, username=username, password=password) # Check if username and password are correct, returning User object if so
        # User objects are the core of the authentication system. They typically represent the people interacting with 
        # your site and are used to enable things like restricting access, registering user profiles, 
        # associating content with creators etc. Only one class of users exists in Django's authentication framework, 
        # i.e., 'superusers' or admin 'staff' users are just User objects with special attributes set, not different classes of User objects.
        # The primary attributes of the default user are: username, password, email, first_name, last_name.
        
        if user is not None:                                 
            # If you want to attach an authenticated user to the current session, use "login()""  to log a user in from a view.
            # It takes an HttpRequest object and a User object. "login()" saves the user's ID in the session, using Django's session framework.
            login(request, user)                              
            return HttpResponseRedirect(reverse("index"))
        else:                                                
            return render(request, "users/login.html", {
                "message": "Invalid Credentials"
            })
    return render(request, "users/login.html")  # # We can also not pass variables to the template if I don't actually need them.

def logout_view(request):
    logout(request)       # "logout()" takes an HttpRequest object and has no return value.
    return render(request, "users/login.html", {
        "message": "Logged Out"
    })