# This file will contain a number of different views, and we can think of a view as one page the user might like to see. 
# We need to tell the app when should you actually run the following functions and what URL is the user going to visit. 
# And this is where we begin to create some URL configuration, 
# some sort of setting to tell Django when a particular URL is visited, then this function should be run.
# So we need to create another "urls.py" file for this particular app.
from django.http import HttpResponse
from django.shortcuts import render

# When a page is requested, Django creates an "HttpRequest" object that contains metadata about the request. 
# Then Django loads the appropriate view function, passing the "HttpRequest" as the first argument to the view function. 
# Each view function is responsible for returning an "HttpResponse" object
def index(request):
    return render(request, "hello/index.html") # Use the "render" function to the template. 
                                               # Note that create a folder called "templates" inside this app ("hello" folder), 
                                               # and create a folder called "hello" (this app's name) within that, 
                                               # then add a file called "index.html". So we can render "hello/index.html".
                                               # We may have multiple different index.html files in multiple different apps. 
                                               # To make sure they don't conflict with each other, the best practice is to use "<APP_NAME>/index.html". 
                                               # That is why we create another "hello" folder in "templates".

def david(request):
    return HttpResponse("Hey, David!") # Use HttpResponse (a very simple response that includes a response code of 200 
                                       # and a string of text that can be displayed in a web browser) to return a http response of "Hello, David!".

def greet(request, name):
    # Here the third argument is passed into "render" which is called "context". 
    # In this context, we can provide information that we would like to have available within the HTML files. 
    # This context takes the form of a Python dictionary, and the variable must be consistent with the template variable (here is "name").
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })