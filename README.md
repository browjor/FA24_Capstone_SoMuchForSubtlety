# 2024 Capstone Project - TrafficLouisville

## Team Name: *So Much For Subtlety*
- John Brown
- Aaron O'Brien
- Mason Napper

Our project is called TrafficLouisville, a system that aims to give timely information about the density of traffic on the major highways of Louisville, KY through a simple map interface that can be accessed through the Internet. TrafficLouisville will not be a commercial system, although it could be monetized through ad-revenue, and is not intended to be used in critical applications. Traffic Louisville is an academic project that illustrates potential applications of software development and machine learning applications.

### Project Description
- TrafficLouisville can be characterized as a multi-component hardware software system consisting of a Python-Flask server (the backend) hosted on personally-owned software that will communicate with a web application hosted on Vercel, a cloud platform (the frontend).
- For a data source, TrafficLouisville will download images obtained from public cameras owned by KYTC (Kentucky Transportation Cabinet) at their respective URLs, at a total request rate of one image every five seconds. Each request will be for a different camera, with a queue that spans roughly fifty cameras, meaning that the refresh rate for our map will be five minutes for a particular camera on a section of highway.
- The backend server will download an image, and queue it for processing with machine learning, specifically Yolov8 image classification. In terms of preparing Yolov8 for classifying particular images, training will be needed to generate a set of model-weights for each specific camera viewpoint, and calibrated for day/night/rain conditions.
- After an estimate of how many vehicles are on the road is compared with baselines and a density figure is generated, the server will send the data for a specific camera to the Vercel-hosted frontend. Here, a heat-map or other relevant map will show the data.
- For the purpose of security, we plan on implementing a reverse proxy that will be used to secure the backend server and frontend.
![image](https://github.com/user-attachments/assets/85fb54b0-dbbd-49ff-834a-96dc3be81432)




