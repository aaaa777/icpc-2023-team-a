import cv2
import numpy as np

DNN_MODEL_PATH =  'FastAPI/dnn_model/'

class VehicleDetector:

    def __init__(self):
        # Load Network

        net = cv2.dnn.readNet(DNN_MODEL_PATH + 'yolov4.weights', DNN_MODEL_PATH + 'yolov4.cfg')
        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(832, 832), scale=1/255)

        # Allow classes containing Vehicles only
        # self.classes_allowed = [2, 3, 5, 6, 7]
        
        self.dict_class = {
            2:'car',
            3:'motorbike',
            5:'bus',
            6:'train',
            7:'truck'
        }
        
        # 2 = car
        # 3 = motorbike
        # 4 = aeroplane
        # 5 = bus 
        # 6 = train
        # 7 = truck
        
        self.classes_allowed = list(self.dict_class.keys())
        

    def detect_vehicles(self, img):
        
        vehicle_count = {
            'car':0,
            'motorbike':0,
            'bus':0,
            'train':0,
            'truck':0
        }
        
        # Detect Objects
        vehicles_boxes = []
        class_ids, scores, boxes = self.model.detect(img, nmsThreshold=0.4)
        for class_id, score, box in zip(class_ids, scores, boxes):
            if score < 0.5:
                # Skip detection with low confidence
                continue

            if class_id in self.classes_allowed:
                vehicles_boxes.append(box)
                vehicle_count[self.dict_class[class_id]] += 1
                
        # print(vehicles_boxes)
        return {
            'vehicles_boxes': vehicles_boxes,
            'vehicle_type': vehicle_count
        }

