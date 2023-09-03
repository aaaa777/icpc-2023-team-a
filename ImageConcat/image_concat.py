import cv2
import numpy as np

# โหลดรูปภาพหลายรูปที่มุมมอง 90 องศา
input_image_paths = ['test.jpg', 'test.jpg', 'test.jpg','test.jpg']  # แก้ไขที่ตั้งของรูปภาพ
ninety_degree_images = [cv2.imread(path) for path in input_image_paths]

# สร้างรูปภาพใหม่โดยการทำซ้ำรูปภาพที่มุมมอง 90 องศาแนวนอน
output_image = np.concatenate(ninety_degree_images, axis=1)

# แสดงผลลัพธ์
cv2.imshow('Merged Image', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


