import os
from camera_list import CameraList

base_directory = 'C:\\Users\\johnb\\PycharmProjects\\FA24_Capstone_SoMuchForSubtlety\\backend\\local_processing\\temp_storage'

for camera in CameraList:
    subdirectory_path = base_directory + '\\' + str(camera[0])
    os.makedirs(subdirectory_path)