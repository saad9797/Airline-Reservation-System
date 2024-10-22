from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


from .models import Flight
from .models import Passenger
# Create your views here.

def index(request):
    return render(request, "flights/index.html" ,{
        "flights" : Flight.objects.all()
    })

def flight(request, flight_id):
    # flight = Flight.objects.get(pk=flight_id) -> if object not found it throws a does not exist exception and next line will not be reached so in tests.py we cannot display the error so to Handle this exact scenario

    flight = get_object_or_404(Flight, pk=flight_id)
    
    return render(request, "flights/flight.html", {
        "flight" : flight,
        "passengers" : flight.passengers.all(),
        "non_passengers" : Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=(request.POST["passenger"]))  
        # name of input field is passenger when posted
        passenger.flights.add(flight)

        return HttpResponseRedirect(reverse("flight",args=(flight.id,)))
