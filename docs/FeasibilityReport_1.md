# Feasibility Report #1

#### 1.

- Our project is called TrafficLouisville, a system that aims to give timely information about the density of traffic on the major highways of Louisville, KY through a simple map interface that can be accessed through the Internet. TrafficLouisville will not be a commercial system, although it could be monetized through ad-revenue, and is not intended to be used in critical applications. Traffic Louisville is an academic project that illustrates potential applications of software development and machine learning applications.

#### 2.

- With this end goal in mind, TrafficLouisville can be characterized as a multi-component hardware software system consisting of a Python-Flask server (the backend) hosted on personally-owned software that will communicate with a web application hosted on Vercel, a cloud platform (the frontend).
- For a data source, TrafficLouisville will download images obtained from public cameras owned by KYTC (Kentucky Transportation Cabinet) at their respective URLs, at a total request rate of one image every five seconds. Each request will be for a different camera, with a queue that spans roughly fifty cameras, meaning that the refresh rate for our map will be five minutes for a particular camera on a section of highway.
- The backend server will download an image, and queue it for processing with machine learning, specifically Yolov8 image classification. In terms of preparing Yolov8 for classifying particular images, training will be needed to generate a set of model-weights for each specific camera viewpoint, and calibrated for day/night/rain conditions.
- After an estimate of how many vehicles are on the road is compared with baselines and a density figure is generated, the server will send the data for a specific camera to the Vercel-hosted frontend. Here, a heat-map or other relevant map will show the data.
- For the purpose of security, we plan on implementing a reverse proxy that will be used to secure the backend server and frontend.

### 3.

- This project should be looked at as very positive by society. It should not affect any jobs, but should possibly help traffic directors and/or police officers as they could check it out and see potentially traffic-heavy areas and focus their attentions there. The premise is quite simple for users, as all they need to do is visit the site and take a look at the heatmap which will tell them where traffic is heavier.

### 4.

- Cost should not be an issue as this project will be using a remote desktop to store the image and then evaluate it using a machine learning program, which will then send the image back off. This eliminates the need to use a server which can get a bit pricy. This project won't necessarily eliminate any other costs from other processes that may be involved with it.

### 5. 

- There are many freely accessible products on the market that are similar to TrafficLouisville, and almost everyone with the required technology uses them while traveling roads unknown. These competitors, commonly known as Google Maps and Apple Maps, estimate traffic flow while users are engaged in navigation. Both products use the GPS data that is shared with the respective navigation software to track the speed of traffic flow (Apple, 2023). Google takes this a step further by saving this information and implementing A.I. to predict how traffic will accumulate based on previous trends (Lau, 2020). TrafficLouisville is not using real-time data, which leads one to think it could never hold a candle to the competition; however, this could not be further from the truth. These tech giants have overlooked the obvious fact that not every vehicle on the road has their software running. By utilizing the feeds from traffic cameras, TrafficLouisville can confidently claim that no car will be left behind. This increased accuracy of traffic flow estimation will surely draw in customers. 

References: 

Apple. (2023, December 11). Apple Legal. https://www.apple.com/legal/privacy/data/en/apple-maps/ 

Lau, J. (2020, September 3). Google Maps 101: How AI helps predict traffic and determine routes. Google. https://blog.google/products/maps/google-maps-101-how-ai-helps-predict-traffic-and-determine-routes/


### 6.

- Many considerations have been made in both the business and technical aspects of TrafficLouisville's development. Most recently the team made the conscious decision to part together a server they could call their own rather than pay a monthly fee to rent one from another business. This was strictly a financial decision, renting a server would have cost the team anywhere from thirty dollars per month for a machine with no GPU to three hundred dollars per month for a machine with a GPU. Knowing that TrafficLouisville's ML component, YOLOv8, would gain a significant speedup from GPU acceleration the team decided to source their own parts as renting was out of their budget. For only fifteen dollars the team was able to build a GPU enabled server perfect for the job, repurposing spare machines and parts that had already been acquired. 
- A technical consideration that had to be made was choosing the optimal machine learning component for image recognition. Two frontrunners were Cascade R-CNN and YOLOv8. Cascade R-CNN is known for high accuracy and precision, but this comes at a high cost of processing power and time. YOLOv8 on the other hand is known for its speed, versatility, and simplicity. Even if it may have lower accuracy than Cascade R-CNN, the team behind TrafficLouisville will be able to train their own custom models tailored to each camera and the possible weather conditions. Additionally, the speedup gained from utilizing YOLOv8 over Cascade R-CNN will make a significant impact on TrafficLouisville's speed and responsiveness. Currently, TrafficLouisville is planned to cover fifty-four traffic cameras around Louisville that update every ten seconds. If the backend cannot process this load within the timeframe then the software will phase out of sync with the cameras resulting in skipped frames of data.


### 7. 
- In terms of the project outcome, risks relevant to our project include scheduling and technical risks. If we don't properly plan for the development of TrafficLouisville, then we may over estimate the amount of time we have to complete it, or improperly estimate what exactly is needed at each stage of development. Technical risks in our project would include unforseen complexity in the moving parts of our project, specifically between the Vercel frontend and the backend Flask server. There may also be the possibility that our source of images will not continue to be public, or are inaccessible for a period of time. As this is unlikely, we will explore our options and decide at the time what the best path is.
- As our system won't be used in critical applications or for monetary purposes, the highest risks we are concerned with are mainly security related. A breach of security could result in violation of the team's privacy, the use of their equipment for malicious purposes, and the loss of personal equipment used in developing and deploying this project. We will give our best attempt at securing the web server with a reverse proxy and the use of HTTPS.

