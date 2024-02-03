# This file will contain a number of different views, and we can think of a view as one page the user might like to see. 
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# This function, by convention, takes as argument a request argument.
# And this is going to represent the HTTP request that the user made in order to access our web server. 
def index(request):
    # We need to tell the app when should you actually run this function and what URL is the user going to visit. 
    # And this is where we now begin to create some URL configuration, 
    # some sort of setting to tell Django when a particular URL is visited, then this function should be run.
    # So we need to create another "urls.py" file for this particular app.

    return HttpResponse("Hello, world!") # Use HttpResponse (a very simple response that includes a response code of 200 
                                         # and a string of text that can be displayed in a web browser) to return an http response of "Hello, World".

def brian(request):
    return HttpResponse("Hello, Brian!")

def greet(request, name):
    return HttpResponse(f"Hello, {name.captialize()}!")