import cv2
import glob
from FastAPI.src.vehicle_detector import VehicleDetector


class VehicalCounting :
        
    def __init__(self,folder_path):
        # Load Veichle Detector
        self.vd = VehicleDetector()
        self.folder_path = folder_path
    
    def set_folder_path(self,path):
        self.folder_path = path
    
    
    def Count(self):
        
        total_vehicle_count = {
            "car":0,
            "motorbike":0,
            "bus":0,
            "train":0,
            "truck":0
        }
        
        vehicle_count_list = [];
        
        # Load images from a folder
        print(self.folder_path)
        images_folder = glob.glob(self.folder_path+ "\*.jpg")
        print("reading image from \n" + self.folder_path )
        
        
        
        # Loop through all the images
        for img_path in images_folder:
            vehicles_folder_count = 0
            print("Img path", img_path)
            img = cv2.imread(img_path)

            vehicle_boxes,vehicle_count = self.vd.detect_vehicles(img).values()
            
            total = len(vehicle_boxes)
            # Update total count
            vehicles_folder_count += total

            # draw box and show the images
            # for box in vehicle_boxes:
            #     x, y, w, h = box

            #     cv2.rectangle(img, (x, y), (x + w, y + h), (25, 0, 180), 3)

            #     cv2.putText(img, "Vehicles: " + str(vehicle_count), (20, 50), 0, 0.7, (100, 200, 0), 3)

            # cv2.imshow("Cars", img)
            # cv2.waitKey(1)
            
            vehicle_count_list.append(vehicle_count);
        
        
        for Vcount in vehicle_count_list :
            for key in list(Vcount.keys()):
                total_vehicle_count[key] += Vcount[key]
        
        
        return total_vehicle_count