from ultralytics import YOLO
from backend.local_processing.models.BoundingBoxes import save_detections_to_disk
import cv2, torch

enable_grayscale = True

def preprocess_image(image):
    preprocessed_image = cv2.imread(image)
    preprocessed_image = cv2.resize(preprocessed_image, (640, 640))
    if enable_grayscale:
        preprocessed_image = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2GRAY)
        preprocessed_image = cv2.cvtColor(preprocessed_image, cv2.COLOR_GRAY2BGR)
    return preprocessed_image

def infer(image, model_weights_path):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = YOLO(model_weights_path).to(device)
    results = model(image)
    return results[0].boxes.data

def extract_vehicle_count(results, confidence):
    vehicles = 0
    for detection in results:
        if detection[4] >= confidence:
            vehicles += 1
    return vehicles

def process_image(image_path, model_weights_path, confidence, save_to_disk, model_name, conditions, image_name):
    image = preprocess_image(image_path)
    detections = infer(image, model_weights_path)
    if save_to_disk:
        #detections are saved as
        save_detections_to_disk(image, image_name, detections, conf=confidence, model_name=model_name, conditions=conditions)
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