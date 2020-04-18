class Car:
    def __init__ (self, vehicle_id, vehicle_status, fleet_id, vehicle_make, licence_plate, current_lat, current_long, last_hb, heartbeat, route):
        #Type : int
        self.vehicle_id = vehicle_id
        #Type: String
        self.vehicle_status = vehicle_status
        #Type : int
        self.fleet_id = fleet_id
        #Type : Vehicle Type
        self.vehicle_make = vehicle_make
        #Type : Boolean
        self.license_plate = licence_plate
        #Type : Float
        self.current_lat = current_lat
        # Type : Array
        self.current_long = current_long
        # Type : Boolean
        self.last_hb = None
        # Type : Boolean
        self.heartbeat = True

        self.route = []



    def __str__(self):

        vehicle_information = "   :: Vehicle Information ::"+ "\n"+" Vehicle ID :: "+ str(self.vehicle_id)+"\n"+" Fleet ID :: "+ str(self.fleet_id)+"\n"+" Vehicle Make :: "+ str(self.vehicle_make)+ "\n"+" Licence Plate # :: "+ self.license_plate+ "\n"+" Current Lat :: "+ str(self.current_lat)+"\n"+" Current Lon :: "+ str(self.current_long)+ "\n"+" Last Heartbeat :: "+ str(self.last_hb)

        return vehicle_information







## TODO: print vehicles by fleet,
