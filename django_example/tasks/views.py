# Django tends to store data inside of tables in the databases. 
# If table hasn't been created, we need to create it by running the command "python3 manage.py migrate" in the terminal. 
# This command will allow us to create all of the default tables inside of Django's database. 
from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

# Django provides an even easier way to collect information from a user: Django Forms.
# Now, we can create a new form within views.py by creating a Python class.
class NewTaskForm(forms.Form):
    # Inside of this class, I need to define all of the fields I would like for this form to have, 
    # all of the inputs that I would like the user to provide. 
    # So I want them to provide the name called "task" which will be a character field, or a "CharField", 
    # meaning I want the user to type in characters. Here I can give this a label, call it "New Task" which will display.
    task = forms.CharField(label="New Task")

    # If we want to add new fields to the form, we can simply add them in views.py without typing additional HTML.
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)
    # Django automatically performs client-side validation, or validation local to the user's machine, 
    # meaning it will not allow a user to submit their form if it is incomplete.
    # You can try that if neither fields is not typed in or the "priority" field is not 1~10, the remainder will pop up.

def index(request):
    # We don't want to create the list "tasks" as a global variable and store the submitted data in it, 
    # so that all of the users who visit the page see the exact same list.
    # We can employ a tool known as sessions to solve this problem 
    if "tasks" not in request.session:  # Check if there already exists a "tasks" key in our session, oththerwise create one.
        request.session["tasks"] = []

    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })

def add(request):
    # Django provides simple server-side validation, or validation that occurs once form data has reached the server
    if request.method == "POST":

        # If I just use NewTaskForm without arguments, that will create a empty form.
        # If the argument is request.POST, where request.POST contains all of the data that the user submitted when they submitted the form. 
        # So I create a form variable by taking all of that data and fill it into this new task form, which will contain now all of the data the user submitted.
        # That is, take in the data the user submitted and save it as form.
        form = NewTaskForm(request.POST)

        # Check if form data is valid (server-side). That is, are they providing all the necessary data in the right format?
        if form.is_valid():  

            # I want to get what "task" they submitted. Because I had a variable here called "task" inside of NewTaskForm,
            # I can go to form.cleaned_data and then task. And then I'll save this as a variable also called "task."
            task = form.cleaned_data["task"]

            # Add the new task to our list of tasks, and you can see it in the route "/tasks".
            request.session["tasks"] += [task] 

            # Return "HttpResponseRedirect" to redirect the user to a particular route, here is "/tasks", 
            # and see your submission of "New Task". Besides, we generally try not to hardcode URLs into our app.
            # The better design would be to give the name of the route and reverse engineer what the route actually is from that. 
            # So we can use the function called "reverse" with the argument "tasks:index" to find out 
            # what the exact URL of the "index" URL for the "tasks" is.
            return HttpResponseRedirect(reverse("tasks:index"))

        # If the form is valid, we take the data from the form, get the "task", save it inside the variable "tasks", and add it to the list "tasks".
        # Else if the form is not valid, we go ahead and render that same add.html file back to them.
        # But instead of providing a new form back to them, we will send back the existing form data back to them. 
        # So we can display information about any errors that might have come up.
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "tasks/add.html", {
                # When I render "add.html", I need to add some context and say, 
                # give this template access to a variable called "form" which will just be a new task form. 
                # So I'm going to create a new task form, pass it into the "add.html" template.
                "form": form
            })
            # You can go to this page to fill out the "New Task" field and type a number between "min_value" and "max_value" in the "Priority" field.
            # Then change "min_value" or "max_value" in this file such that this number is not in the previous range, and go back to the page to submit. 
            # You will see an error occurs. That is why we generally want both client- and server-side validation. 
            # Because client-end version may be not the up-to-date, server-side should check again to avoid errors.

    # Mean if method is GET. If the user just tried to get the page rather than submit data to it, 
    # then we're just going to render to them an empty form. 
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()  # Create a empty form
    })
