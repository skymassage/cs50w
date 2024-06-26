from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Flight, Airport, Passenger

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id) 
    except Flight.DoesNotExist:
        raise Http404("Flight not found.")
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()          
    })


def book(request, flight_id):
    if request.method == "POST":
        try:
            passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
            flight = Flight.objects.get(pk=flight_id)
        # A Python KeyError exception is what is raised when you try to access a key that isn't in a dictionary.
        except KeyError: 
            # "HttpResponseBadRequest" acts just like HttpResponse but uses a 400 status code.
            return HttpResponseBadRequest("Bad Request: no flight chosen")
        # Django provides a DoesNotExist exception as an attribute of each model class to identify the class of object 
        # that could not be found, allowing you to catch exceptions for a particular model class. 
        except Flight.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: flight does not exist")
        except Passenger.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: passenger does not exist")
        
        passenger.flights.add(flight)                       
        
        return HttpResponseRedirect(reverse("flights:flight", args=[flight.id]))

        
