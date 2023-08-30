import cv2
import glob
from vehicle_detector import VehicleDetector

class VehicalCounting :
        
    def __init__(self,folder_path):
        # Load Veichle Detector
        self.vd = VehicleDetector()
        self.folder_path = folder_path
    
    def set_folder_path(self,path):
        self.folder_path = path
    
    
    def Count(self):
        # Load images from a folder
        images_folder = glob.glob(self.folder_path + "*.jpg")
        
        
        # Loop through all the images
        for img_path in images_folder:
            vehicles_folder_count = 0
            print("Img path", img_path)
            img = cv2.imread(img_path)

            vehicle_boxes = self.vd.detect_vehicles(img)
            vehicle_count = len(vehicle_boxes)

            # Update total count
            vehicles_folder_count += vehicle_count


            # draw box and show the images
            # for box in vehicle_boxes:
            #     x, y, w, h = box

            #     cv2.rectangle(img, (x, y), (x + w, y + h), (25, 0, 180), 3)

            #     cv2.putText(img, "Vehicles: " + str(vehicle_count), (20, 50), 0, 2, (100, 200, 0), 3)

            # cv2.imshow("Cars", img)
            # cv2.waitKey(1)

        print("Total current count", vehicles_folder_count)
        return vehicles_folder_count