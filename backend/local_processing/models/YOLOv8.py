
#pytorch version must be compatible with CUDA driver:
#https://pytorch.org/get-started/locally/
#https://developer.nvidia.com/cuda-11-8-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_network
#use ZLUDA for amd cards

import torch
from ultralytics import YOLO
import os
import json
from backend.local_processing.models import BoundingBoxes

dictionary = [(0.0, 'person'),
              (1.0, 'bicycle'), #ommit
              (2.0, 'car'),
              (3.0, 'motorcycle'),
              (5.0, 'bus'),
              (6.0, 'train'), #ommit
              (7.0, 'truck')]

def process_image(image):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    #print(torch.version.cuda)
    #print("Using device: " + device)
    #./ runs / detect / train6 / weights / best.pt
    model = YOLO('C:\\Users\\johnb\\PycharmProjects\\FA24_Capstone_SoMuchForSubtlety\\backend\\local_processing\\models\\best.pt').to(device)
    results = model.predict(image, conf=0.3)
    #print(results)
    #print(results[0].boxes.data)
    return results[0].boxes.data

#could implement a counter instead
def extract_data(results):
    unformatted_data = []
    for detection in results:
        for entry in dictionary:
            if detection[5] == entry[0]:
                unformatted_data.append(entry[1])
    #print(unformatted_data)
    return len(unformatted_data)

def write_json(data, camera_id):
    formatted_data = {
        "numberofvehicles": data
    }
    json_object = json.dumps(formatted_data, indent=4)
    if not os.path.exists('./json'):
        os.makedirs('./json')
    with open('./json/' + camera_id + '.json', 'w') as outfile:
        outfile.write(json_object)


#if not os.path.exists('./images'):
#    os.makedirs('./images')

#for image_path in os.listdir('./images'):
#    if image_path.endswith('.png'):
#        detections = process_image('./images/' + image_path)
#        plot_bboxes('./images/' + image_path, detections, conf=0)
#        data = extract_data(detections)
#        print(data)
#        write_json(data, image_path[0:len(image_path)-4])


#image1 = process_image("./images/test.jpg")
#extract_data(image1)
#image2 = process_image("./images/test2.jpg")
#extract_data(image2)
#image3 = process_image("./images/test3.jpg")
#extract_data(image3)
