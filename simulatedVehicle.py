from time import sleep
from datetime import datetime
import json
import requests
import time

#In this context, a simulated vehicle represents vehicles that are actually "running", i.e threaded
class simulatedVehicle:
    def __init__(self, vehicle, threadid):
        self.vehicle = vehicle
        self.threadid = threadid

    def driver(self):
        #print(f'\n{self.vehicle}')
        if self.vehicle.vehicle_status is not 'maintenance':
            if self.vehicle.route:
                nextCoor = self.vehicle.route.pop(0)
                self.vehicle.current_long = nextCoor[0]
                self.vehicle.current_lat = nextCoor[1]
                request_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'+str(self.vehicle.current_long)+','+str(self.vehicle.current_lat)+'.json?access_token=pk.eyJ1IjoiY3N5Y2hldiIsImEiOiJjazZsbmg4c2gwYXU3M21zOG55aTljcTBuIn0.G5UXjF-3_0mXKo6huFgLwg'
                address_request = requests.get(request_url)
                address_data = address_request.json()
                address = json.dumps(address_data.get("features")[0].get("place_name"))
                print("Current location of vehicle",str(self.vehicle.vehicle_id)," ::", address, "\n")
            if self.vehicle.heartbeat:
                self.heartbeat()


    def heartbeat(self):

        print('\nNow sending a heartbeat for vehicle ',str(self.vehicle.vehicle_id), end='\n')
        now = datetime.now().isoformat()
        #data being sent to supply BE to update vehicle database
        postBody = {
            'vid': self.vehicle.vehicle_id,
            'current_lat': self.vehicle.current_lat,
            'current_lon': self.vehicle.current_long,
            'status': self.vehicle.vehicle_status,
            'last_heartbeat': now
            }
        postBody = json.dumps(postBody)
        #request to update backend
        response = requests.post('https://supply.team22.softwareengineeringii.com/supply/vehicles/upd', postBody)


        #checking for a dispatch
        #if there is a dispatch, vehicle will start moving
        if response.json():
            route = response.json().pop(1)
            route.pop(0)
            self.vehicle.route = route
        else:
            print("ERROR :: ", response.status_code)
