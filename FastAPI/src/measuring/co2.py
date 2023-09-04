
class CO2Counter:

    co2_per_vehicle_list = {
        "car": 0.118,
        "motorbike": 0.104,
        "bus": 0.027,
        "truck": 0.089,
        "train": 0.006,
    }

    def __init__(self):
        self.co2 = 0

    def caluculate(self, vehicle_count_dict):
        for vehicle_type, count in vehicle_count_dict.items():
            if(vehicle_type in self.co2_per_vehicle_list):
                self.co2 += self.co2_per_vehicle_list[vehicle_type] * count
        print(self.co2)
        return self.co2