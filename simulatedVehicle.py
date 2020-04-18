from time import sleep
from datetime import datetime
import json
import requests
import time
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
            if self.vehicle.heartbeat:
                self.heartbeat()


    def heartbeat(self):
        print('I just sent a heartbeat', end='\n\n> Enter another vehicle ! ')
        #change a bit to adapt to hh/mm/ss.ms
        #print("currently sending a heartbeat!!")
        sleep(1)
        now = datetime.now().isoformat()
        postBody = {
            'vid': self.vehicle.vehicle_id,
            'current_lat': self.vehicle.current_lat,
            'current_lon': self.vehicle.current_long,
            'status': self.vehicle.vehicle_status,
            'last_heartbeat': now[now.index('T') + 1:]
            }
        # print(postBody)
        postBody = json.dumps(postBody)
        # print(postBody)
        response = requests.post('https://supply.team22.softwareengineeringii.com/supply/vehicles/upd', postBody)
        # print(response.status_code)

        if response.json():
            self.vehicle.route = response.json()['route']
        else:
            #print("ERROR :: ", response.status_code)
            variable = 8
