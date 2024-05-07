import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Email


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mail/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "mail/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mail/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(email, email, password) # We set the username to email here.
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "mail/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mail/register.html")


def index(request):
    if request.user.is_authenticated:
        return render(request, "mail/inbox.html")
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required
def mailbox(request, mailbox): # Display corresponding mail items when entering different mailboxes.
    # We must first filter to identify emails related to the logged in user, so each filter requires "user==request.user".
    if mailbox == "inbox":
        emails = Email.objects.filter(
            user=request.user, recipients=request.user, archived=False
        )
    elif mailbox == "sent":
        emails = Email.objects.filter(
            user=request.user, sender=request.user
        )
    elif mailbox == "archive":
        emails = Email.objects.filter(
            user=request.user, recipients=request.user, archived=True
        )
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400) # "JsonResponse" is an HttpResponse subclass that helps to create a JSON-encoded response.
        # If you request an invalid mailbox (anything other than inbox, sent, or archive), you'll instead get back the JSON response {"error": "Invalid mailbox."}.

    emails = emails.order_by("-timestamp").all() # The minus '-' inside of "-timestamp" means the descending order.

    # In order to serialize objects other than dict you must set "safe=False", otherwise a TypeError will be raised. 
    # Note that an API based on dict objects is more extensible, flexible, and makes it easier to maintain forwards compatibility.
    # Therefore, you should avoid using non-dict objects in JSON-encoded response.
    return JsonResponse([email.serialize() for email in emails], safe=False) 
    # For example, if you send a GET request to "/emails/inbox", you might get a JSON response like the below (representing two emails): 
    # [{"id": 100, "sender": "foo@example.com", "recipients": ["bar@example.com"], "subject": "Hello!", 
    #   "body": "Hello, world!", "timestamp": "Jan 2 2020, 12:00 AM", "read": false,"archived": false},
    #  {"id": 95, "sender": "baz@example.com", "recipients": ["bar@example.com"], "subject": "Meeting Tomorrow",
    #   "body": "What time are we meeting?", "timestamp": "Jan 1 2020, 12:00 AM", "read": true, "archived": false}]


# For POST and PUT requests, Django requires a CSRF token to guard against potential cross-site request forgery attacks
# In this project, we've intentionally made the API routes CSRF-exempt, so you won't need a token. 
# In a real-world project, though, always best to guard against such potential vulnerabilities!
@csrf_exempt # "@csrf_exempt" marks a view as being exempt from the protection ensured by the middleware
@login_required
def compose(request): # Store email information in the database when sending emails.
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400) 
    
    # Access the body of the request we sent by "<request>.body" which we have written inside of "fetch()" in the JS code.
    data = json.loads(request.body) # "json.loads()" parses a valid JSON string and convert it into a Python Dictionary.

    # Use ".get(<key>)" in Python to get the key value of the JSON object. If the key doesn't exist, ".get(<key>)" returns None. 
    # And we can add a second argument to specify what will be returned if the key is not found. 
    # For example, ".get(<key>, "Error")" will return a string "Error" if the key was not found.
    # Note that data.get("recipients") is a string because it was converted into a string by ".stringify" in JS code.
    emails = [email.strip() for email in data.get("recipients").split(",")] # Split the string into a list using comma as a separator.
    if emails == [""]:
        return JsonResponse({"error": "At least one recipient required."}, status=400)

    if request.user.email in emails:
        return JsonResponse({"error": "You cannot send the email to yourself."}, status=400)

    # "emails" is a list containing recipient addresses, and these addresses are just strings.
    # We need to create another list containg the same the recipients, but they are the User class objects.
    recipients = []
    for email in emails:
        try:
            user = User.objects.get(email=email)
            recipients.append(user) # "recipients" is a list of the User class objects containing the attributes: username, email, password.
        
        # Django provides a DoesNotExist exception as an attribute of each model class to identify the class of object 
        # that could not be found, allowing you to catch exceptions for a particular model class. 
        except User.DoesNotExist: 
            return JsonResponse({"error": f"User with email {email} does not exist."}, status=400)

    subject = data.get("subject", "")
    body = data.get("body", "")

    # Create one email for each recipient, plus sender
    users = set() # Create an empty set. 
    users.add(request.user)
    users.update(recipients) # ".update" inserts the items from the list "recipients" into the set "users".
    for user in users:
        email = Email(
            user=user,
            sender=request.user,
            subject=subject,
            body=body,
            read=user == request.user # 
        )
        email.save()
        for recipient in recipients:
            email.recipients.add(recipient)
        email.save()
    # This means if the sender sends an email to N other recipients, 
    # we will create N rows in the database's email model.
    # For these rows, all fields except "user" and read"" are the same.
    # The "user" field contains only one value which would be the email address of sender or recipients.
    # And the "read" field would be True if the "user" field is same as the "sender" field 
    # ,i.e., user and sender ((request.user)) are the same.

    return JsonResponse({"message": "Email sent successfully."}, status=201)


@csrf_exempt 
@login_required
def email(request, email_id): # Get the email information based on the email ID (GET method). Mark email as read/unread or as archived/unarchived (PUT method).
    try:
        email = Email.objects.get(user=request.user, pk=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)
    
    if request.method == "GET": # Return email contents
        return JsonResponse(email.serialize())

    # The HTTP request POST method sends data to a server in a request body. 
    # HTML form data is typically sent to the server using a POST request. 
    # The server can use this data to add the sent data to a database.
    # The HTTP PUT method is used to create a new resource or replace a resource. 
    # It's similar to the POST method, in that it sends data to a server, but it's idempotent. 
    # This means that the effect of multiple PUT requests should be the same as one PUT request.
    # For example: 
    #   You may have a book review app that has an "/add_book" API route that you could send book data to. 
    #   The sent book data can then be added to a database on the server. 
    #   Making multiple POST requests to this API will create multiple book entries in the database.
    #   Your book review app may also have an "/edit_book/<id>" API route that allows you to edit a book by its ID. 
    #   API requests to this route would be suited to PUT requests that will replace the book information in the database with the data in the request payload. 
    #   Multiple PUT requests to edit the book data will result in the same data change as one PUT request to edit the data.
    # However that these definitions are only defined by the HTTP specifications for POST and PUT.
    # In reality, it is up to software engineers to implement POST and PUT into apps as recommended by the specification, 
    # and a correct implementation is not always guaranteed.
    elif request.method == "PUT": # Update whether email is read or should be archived
        data = json.loads(request.body)
        if data.get("read") is not None:
            email.read = data["read"]
        if data.get("archived") is not None:
            email.archived = data["archived"]
        email.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

