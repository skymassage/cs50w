# Django has one "urls.py "file that works for the entire project. But typically we'll have each app contain its own "urls.py" files. 
# So we can have each of those individual apps have its own "urls.py" file to control what URLs are available for that particular app. 

from django.urls import path 
from . import views # "from ." means from the current directory.

 # "urlpatterns" is a list of all of the allowable URLs that can be accessed for the particular app.
urlpatterns = [
    # The "path" function is the path converter
    # "path" gives us the ability to reroute URLs and has two or three arguments: 
    # 1. A string representing the URL path (here is the empty string which means nothing at the end of the route), 
    # 2. A function from "views.py" that we wish to call when this URL is visited. 
    #    That is, what view should be rendered when this URL is visited. 
    # 3. A name for that path or URL. This argument is optional. 
    #    Giving the name of the view to a particular URL pattern makes it easy to reference it from other parts of the app.
    # So if I want to render my "index" view (the "index" function in "views.py"). 
    # Then what I want to render when someone visits this URL (the empty URL) is going to be views.index. 
    path("", views.index, name="index"),           # Add "/hello" to the url of the home page to see the result.
                                                   # When you go to the root URL (homepage), you will encounter 404,
                                                   # because we don't set "path('', include("<APP_NAME>.urls"))" for the root URL 
    
    path("hey/david", views.david, name="david"), # Add "/hello/hey/david" to the url of the home page to see the result.

    # Use angle brackets "<>" to capture the values from the URL and pass them to the second arugment as the parameter to this function.
    # "str" inside of "<>" specify the type of the captured value "name".
    # If the type isn't specifed, the captured value type will be string by default. 
    # Note that the captured value must be named as the parameter of the called function so as to pass it to that funciton in views.py.
    # So here means that we capture the value "name" from the URL and convert it to a string, then this value is passed to the "greet" function in views.py as its parameter "name"
    path("<str:name>", views.greet, name="greet"), # Add "/hello/<name>" to the url of the home page to see the result, where "<name>" you can type anything you want.
]