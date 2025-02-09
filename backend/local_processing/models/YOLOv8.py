from ultralytics import YOLO
from BoundingBoxes import save_detections_to_disk
import cv2

enable_grayscale = True

def preprocess_image(image):
    preprocessed_image = cv2.imread(image)
    preprocessed_image = cv2.resize(preprocessed_image, (640, 640))
    if enable_grayscale:
        preprocessed_image = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2GRAY)
        preprocessed_image = cv2.cvtColor(preprocessed_image, cv2.COLOR_GRAY2BGR)
    return preprocessed_image

def infer(image, model_weights_path):
    model = YOLO(model_weights_path)
    results = model(image)
    return results[0].boxes.data

def extract_vehicle_count(results, confidence):
    vehicles = 0
    for detection in results:
        if detection[4] >= confidence:
            vehicles += 1
    return vehicles

def process_image(image_path, model_weights_path, confidence, save_to_disk):
    image = preprocess_image(image_path)
    detections = infer(image, model_weights_path)
    if save_to_disk:
        save_detections_to_disk(image, image_path, detections, conf=confidence)
    data = extract_vehicle_count(detections, confidence)
    return data

'''
import os

model_weights = 'All_Grayscale.pt'
images_directory = './NighttimeImages/'

for image_file in os.listdir(images_directory):
    if image_file.endswith('.png'):
        returned_data = process_image(images_directory + image_file, model_weights, 0.3, True)
        print(returned_data)
'''