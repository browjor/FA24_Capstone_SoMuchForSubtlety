from ultralytics import YOLO
import cv2
import math

enable_local_testing = True

if enable_local_testing:
    # pytorch version must be compatible with CUDA driver:
    # https://pytorch.org/get-started/locally/
    # https://developer.nvidia.com/cuda-11-8-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_network
    import torch
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    import os
    from BoundingBoxes import plot_bboxes
    model_weights_path = './datasets/DaytimeDatasetYolov8n/best.pt'
    images_directory = './DaytimeImages/'

sigma = 2
kernel_size = int(2 * math.ceil(2 * sigma) + 1)

confidence = 0.3

enable_blur = False
enable_grayscale = False

def set_preprocessing_flags(model_weights_path):
    global enable_blur, enable_grayscale
    if "daytime" in model_weights_path.lower():
        enable_blur = False
        enable_grayscale = False
    return

def gaussian_blur_image(image):
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    return blurred_image

def grayscale_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    reformatted_gray_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    return reformatted_gray_image

def resize_image(image):
    resized_image = cv2.resize(image, (640, 640))
    return resized_image

def preprocess_image(image):
    preprocessed_image = cv2.imread(image)
    preprocessed_image = resize_image(preprocessed_image)
    if enable_grayscale:
        preprocessed_image = grayscale_image(preprocessed_image)
    if enable_blur:
        preprocessed_image = gaussian_blur_image(preprocessed_image)
    return preprocessed_image

def infer(image, model_weights_path):
    model = YOLO(model_weights_path)
    if enable_local_testing:
        model = model.to(device)
    results = model(image)
    return results[0].boxes.data

def extract_vehicle_count(results):
    vehicles = 0
    for detection in results:
        if detection[4] >= confidence:
            vehicles += 1
    return vehicles

def process_image(image_path, model_weights_path):
    set_preprocessing_flags(model_weights_path)
    image = preprocess_image(image_path)
    detections = infer(image, model_weights_path)
    if enable_local_testing:
        plot_bboxes(image, detections, conf=confidence)
    data = extract_vehicle_count(detections)
    return data

if enable_local_testing:
    for image in os.listdir(images_directory):
        if image.endswith('.png'):
            data = process_image(images_directory + image, model_weights_path)
            print(data)