class Event:
    def __init__(self, startTime, endTime):
        self.startTime = startTime
        self.endTime = endTime
        self.venue = []

    def addVenue(self, Venue):
        self.venue.append(Venue)


class Venue:

    def __init__(self, name):
        self.name = name
        self.address = []

    def getaddress(self, address1):
        self.address.append(address1)

class Address:

    def __init__(self, street, city, country, state, zipcode):
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode

address = Address("103/2/e A.k. Mukherjee Road", "Kolkata", "West Bengal", "India", "700090")
venue1 = Venue("Monoroma Palace")
event1 = Event("2pm", "8pm")
venue1.getaddress(address)
event1.addVenue(venue1)
print("Start Time {}  End Time {}".format(event1.startTime, event1.endTime))
for eventvenue in event1.venue:
    print(eventvenue.name)
    for address in venue1.address:
        print(
            "{}, {}, {}, {}, {}".format(address.street, address.city, address.state, address.country, address.zipcode))
