
#import Car
import requests
import json
import threading
from Car import Car
from simulatedVehicle import simulatedVehicle
from time import sleep
from prettytable import PrettyTable
import sys

vehicle_list = []
vehicle_db_dictionary = {}
threaded_vehicles = {}

class Controller:
    def __init__(self):
        self.vehicleArr = []
        self.models = []

    def startThreads(self):
        while True:
            if len(self.vehicleArr) != 0:
                for index, vehicle in enumerate(self.vehicleArr, 1):
                    self.models.append(simulatedVehicle(vehicle, index))
            for model in self.models:
                thread = threading.Thread(target=model.driver, name=f"model-{model.threadid}")
                thread.start()
            sleep(3)
            self.models = []



def main():
    print("\t*************************************************")
    print("\t**** Welcome to the WeGo Vehicle Simulator!  ****")
    print("\t*************************************************")
    print("\t*** Any time you want you quit just press 'Q' ***")
    print("\t*************************************************")
    print("\t********* Retrieving your vehicles .... *********")
    global vehicle_db_dictionary

    vehicle_db_dictionary = retrieveVehicles()
    printCurrentState(vehicle_db_dictionary)
    updatingVehicles = True
    #threading.Thread(target=heartbeat_manager).start()

def printCurrentState(vehicle_dict):
    simulatorOptions = PrettyTable()
    simulatorOptions.field_names = ["Simulator Options", "Description", "Command"]
    carTable = PrettyTable()
    carTable.field_names = ["Vehicle ID", "Status", "Fleet ID", "Make", "Licence Plate", "Current Longitude", "Current Latitude", "Last Heartbeat"]
    simulatorOptions.add_row(["Kill Heartbeat", "Kill the heartbeat of a vehicle", "Enter vehicle id of a currently "])
    simulatorOptions.add_row(["Start Heartbeat", "Start the heartbeat of a vehicle, fleet, or all vehicles", "Enter a vehicle ID"])

    # keep asking user for input
    # if they do anything but start route, do backend data changes
    # if they do start route:
    #   create new thread for that car with function executeCarRoute
    for car in vehicle_dict.values():
        carTable.add_row([car.vehicle_id,car.vehicle_status,car.fleet_id,car.vehicle_make,car.license_plate,car.current_long,car.current_lat,car.last_hb] )
    print(carTable)
    print("\n")
    print(simulatorOptions)

#returns a dictionary of vehicles of type Car
#Want to make a thread for each of these? Don't know if I should do this inside this function or somewhere else
#Wherever I end up making the vehicle threads, have those threads send updates to the db updating it's car Information
#However this is done Here's what needs to get done:
    #for every vehicle, a request should be sent to the BE to update the info of that vehicle in the DB
    #how that gets done with threading i'm not sure yet
def retrieveVehicles():
    request_vehicles = requests.get("https://supply.team22.softwareengineeringii.com/supply/vehicles")
    #v_list = []
    v_dict = {}
    if request_vehicles:
        vehicles = request_vehicles.json()
        vehicles.pop(0)
        for v in vehicles:
            v_id = v.get("vehicleid")
            v_stat = v.get("status")
            f_id  = v.get("fleetid")
            v_make = v.get("make")
            l_plate = v.get("licenseplate")
            c_long = v.get("current_lon")
            c_lat = v.get("current_lat")
            last_hb = v.get("last_hb")
            heartbeat = True
            route = []
            simulated_vehicle = Car(v_id, v_stat, f_id, v_make, l_plate, c_long, c_lat, last_hb, heartbeat, route)
            v_dict.update({v_id : simulated_vehicle})
        #return v_list
        #for a car to be on it's not in maintenance

        return v_dict
        # for i,j in hb_dict.items():
        #     print("Key :: " + i)
        #     print("\nValue :: " + j)
    else:
        print("ERROR :: ", request_vehicles.status_code)
        print("We were not able to retrieve your vehicles, closing application ... ")
        sys.exit


def view(inputVar):

    print('Input the vehicle id you want to spin up!')
    while True:
        userInput = input("> ")
        #print(threaded_vehicles.get(int(userInput)))
        if userInput.lower() == 'all':
            inputVar.extend([vehicle for vehicle in vehicle_db_dictionary.values()])
        #put something for turnoff heartbeat
        elif threaded_vehicles.get(userInput):
            print("** This vehicle is running! **\n")
            for i in inputVar:
                if(i.vehicle_id==int(userInput)):
                    i.heartbeat = False
                    print("Heartbeat stopped for vehicle ", str(i.vehicle_id))
        else:
            try:
                #vehicle = vehicle_db_dictionary[int(userInput)]
                vehicle = vehicle_db_dictionary.get(int(userInput))
                if (vehicle != None):
                    inputVar.append(vehicle)
                    threaded_vehicles.update({userInput: vehicle})
            except KeyError as ke:
                print(ke)
                print('Key doesn\'t exist in dictionary!')

#Tomorrow! Stop hbs, formatting

#group vehicles by fleet id
#an option to select a fleet and send heartbeats for a fleet
#heartbeat goes in model??
#Always updating position
#For interface: keep track of vehicles being simulated

    #sendHB's??????3
    #getback a status?????
    #logic for checking its status for a routes
    #


#Was trying to flesh out an idea about executing a route, this ideally will be used later?


# If button is pressed, make request for the id of that vehicle ?
# How does this work with threading?? So if I click a button for an option, does it call that function with that car? In that thread?


if __name__ == '__main__':
    main()
    controller = Controller()
    thread1 = threading.Thread(target=controller.startThreads, name="controller")
    thread2 = threading.Thread(target=view, args=(controller.vehicleArr,), name="UI")
    thread2.start()
    thread1.start()
