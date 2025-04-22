# 2024/2025 Capstone Project - TrafficLouisville

## Team Name: *So Much For Subtlety*
- John Brown
- Aaron O'Brien
- Mason Napper


Our capstone project, TrafficLouisville, aims to provide near-real time traffic density visualization for Louisville Metro Highways. Through KYTC highway camera images available over the web, machine learning object detection via YOLOv8, and a custom full stack web architecture, we have developed TrafficLouisville to present an intuitive map that can be used for traffic estimation and analytics.

Installation instructions can be found in INSTALLATION.txt 


### Project Description

TrafficLouisville is designed as multiple independent processes (Python) connected by a database (SQLite) within the backend machine, while a reverse proxy (Caddy) connects the remote frontend (Vercel/React) with the backend server (Flask/Python). Write/read locks among the connections to the database enforce coordination among the backend processes. Secure communications are prioritized via HTTPS, a reverse proxy, and HMAC signature verification of requests and responses between the frontend and backend. Upon request from a browser client, the frontend requests the data for populating the map from the backend, authenticates it, and serves it to the browser client.


- 
![RF3_ComponentDiagram drawio](https://github.com/user-attachments/assets/7fa235c9-0c6b-449c-bf97-b6e43ee4bf0d)

![DeploymentDiagram_2 drawio](https://github.com/user-attachments/assets/fa36cba8-bb24-4693-bbad-12a2554c075c)



