from django.test import TestCase, Client
from django.db.models import Max
from .models import Airport, Flight, Passenger

# Create your tests here.

class FlightTestCase(TestCase):
    
    def setUp(self):
        # setUp is a special function that creates dummy data
        # this is dummy data create to test it does not modify the actual database that users interact with

        #Create Airports :
        a1 = Airport.objects.create(code="AAA", city="cityA")
        a2 = Airport.objects.create(code="BBB", city="cityB")

        #Create Flights :
        Flight.objects.create(origin=a1,destination=a2,duration=100)
        Flight.objects.create(origin=a1,destination=a1,duration=100)
        Flight.objects.create(origin=a1,destination=a2,duration=-100)


    # test airport departures/arrivals working correctly :

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)
   
    # is valid flight :

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight(origin = a1, destination = a2, duration = 100 )
        self.assertTrue(f.is_valid_flight())

    # testing for an invalid flight

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin = a1, destination = a1)
        self.assertFalse(f.is_valid_flight())

    
    def test_invalid_flight_duration(self):
        f = Flight.objects.get(duration = -100)
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        c = Client()
        response = c.get("/flights/")
        self.assertEqual(response.status_code, 200) # response -> ok
        self.assertEqual(response.context["flights"].count(),3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_page(self):
        # Get the maximum ID in the Flight table
        
        maxid = Flight.objects.all().aggregate(Max("id"))["id__max"]
        # aggregate returns a dictionary "id__max" is equal to the max id

        c = Client()
        response = c.get(f"/flights/{maxid+1}")
        
        # Request the page for a flight that does not exist (id: maxid)
        self.assertEqual(response.status_code, 404)


    
    
    def test_flight_page_passenger(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Harry",last="Potter")
        f.passengers.add(p)
        # passengers is a related name in passenger model and so hence forth the related name can be accessed from the class it is related to

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_nonPassenger(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Harry",last="Potter")
        # passenger is created but not added to the flight

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)


