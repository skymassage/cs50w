# Django has one "urls.py "file that works for the entire project. But typically we'll have each app contain its own "urls.py" files. 
# So we can have each of those individual apps have its own "urls.py" file to control what URLs are available for that particular app. 

from django.urls import path 
from . import views # "from ." means from the current directory.

urlpatterns = [   # "urlpatterns" is a list of all of the allowable URLs that can be accessed for this particular app. 
    # The "path" function is the path converter
    # "path" give us the ability to reroute URLs and has two or three arguments: 
    # 1. A string representing the URL path (Here is the empty string which means nothing at the end of the route), 
    # 2. A function from "views.py" that we wish to call when this URL is visited. 
    #    That is, what view should be rendered when this URL is visited. 
    # 3. A name for that path or URL. This argument is optional. 
    #    Giving a name to a particular URL pattern makes it easy to reference it from other parts of the application.
    # So if I want to render my "index" view (the "index" function in "views.py"). 
    # Then what I want to render when someone visits this URL (the empty URL) is going to be views.index. 
    path("", views.index, name="index"),           # Add "/hello" to the url of the home page to see the result.
    path("brian", views.brian, name="brian"),      # Add "/hello/brain" to the url of the home page to see the result.

    # Use angle brackets "<>" to capture the values from the URL and pass them to the second arugment as the parameter to this function.
    # The captured value can optionally include the type. If the type isn't specifed, the captured value will be string by default. 
    # If the captured value is to be used as other types, its type can be converted from string to that type.
    # Note that the captured value must be named as the parameter of the called function so as to pass it to that funciton.
    # Here means that we capture the value "name" from the URL and convert it to a string, then this value is passed to the "greet" function in views.py as its parameter "name"
    path("<str:name>", views.greet, name="greet"),     
]