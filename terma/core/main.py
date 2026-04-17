class Vector 

class Drone:
    def __init__(self, name):
        self.name = name
        self.altitude = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.speed = 0
        self.battery_level = 100


    def get_altitude(self):
        return self.altitude

    def get_position(self):
        return (self.x, self.y, self.z)

    
    def fly(self):
        print(f"{self.name} is flying!")


d1 = Drone("Drone1")
d1.fly()

class FarmerDrone(Drone):
    def __init__(self,name):
        super().__init__(name)
        self.crops = []