# Meeting Minutes

## 9/3/2024
Talk to sexton about tech stack on traffic project

Questions for sexton:

1. Is a digital ocean server appropriate for this level
		- any tips on setting it up?
		- "DO" said it was linux based, do i provide an OS or is there one already there?
		- could i access it with something like putty?

2. is flask a good option for this? it seemed mostly like a html server

### Actionables:
- send email to KYTC on thursday 9/5 clarifying our project

- send email to pittman on thursday 9/12 asking about a good zoom time

## 9/10/2024
Email sent to KYTC as planned

Talked about potential remote server costs, instead agreed to deploy a server on one of Mason's desktops

Desired specs for server would be 10-15 GB SSD (128 economical choice) and 8-16 GB RAM, with possible GPU assistance

Vercel still frontrunner for frontend hosting

Instead of direct KYTC server requests, web scraping may be better option for simplicity

For first report:
JB - Q1,2,7

MN - Q3,4

AB - Q5,6

#### Potential Future Issues:
Day/Night/Rain differences in training/prediction of yolov8 models

This could be solved by training models with particular weights for a particular camera to aid in prediction

### Actionables:
- write script to test if pulling images from urls is feasible

- look into running Python/Flask server on windows

- decide on which project to do

## 9/17/2024

![image](https://github.com/user-attachments/assets/85fb54b0-dbbd-49ff-834a-96dc3be81432)

Discussed plans for traffic project, split up responsibilities
JB - server, manage hardware
AO - manage training of yolov8 models
MN - develop frontend application

### Actionables:
- get local development environments up and running



## 9/24/2024
results from yolov8 general model on highways in good conditions:
![image](https://github.com/user-attachments/assets/becfd035-1abf-4f70-9253-b3b657af1058)
![image](https://github.com/user-attachments/assets/120425b1-8e80-4ee4-9ba2-fcc16bbc2241)
![image](https://github.com/user-attachments/assets/25916569-48e1-42b2-b9ab-8cadfcdaa9a2)

- model training goals:
1. we can have a model weight (meaning multiple weights for various conditions) for every camera, but do we need one?
   - consider having just one model for each condition, blurry camera, daylight, raining, nighttime, snow?
     	- the promising results of the generic yolov8 model support having a model per condition
2. if we did have model weights for various conditions, how would we tell yolov8 when to use a particular model?
   	- formulas that determine when the sun goes down in conjunction with data collected at different times could tell us when car headlights come on and would require a model change
4. for a particular camera, traffic moves in different directions on certain parts of the screen, how do we deal with this?
   - potential options include imposing a filter on a part of the picture that blocks results in a particular direction
   - another option would include arguments to the model that tell it to only report results from a particular part of a picture
     	- this problem involves how we will be reporting data, is our heatmap reporting on traffic going directions or are we just saying that there is a lot of traffic on the highway at this point?
     	- if we implement multiple direction reporting, this will require organization on how the model is applied and how results are determined
5. for training models, how many pictures will be needed to improve the model and therefore accuracy of results?
   - first, we will collect a small number (10) of images from each camera for two conditions (day/night)
   - second, we will select three cameras with a good view and generating weights via training for each of the cameras and condition (6 total sets of pictures)
   - third, we will test the generic yolov8 versus the three models by predicting a test set of pictures
6. how do we deal with abnormal events like construction or traffic accidents?
   - the generic yolov8 models are capable of detecting people. we may be able to use this to signal to the heatmap that the results may be unreliable and show it on hte map

### Update:
- KYTC has emailed us back and given permission for access of their resources with the following conditions:
	- one image per 10 seconds from their servers
   	- suggested long term storage is a BAD idea
   	- all data is under Creative Commons Zero License and KYTC does not warrant the data
   	- to communicate the following message very clearly:
   	  ![image](https://github.com/user-attachments/assets/41a9cef9-ccdb-4b7a-abf4-656eb9d73e63)
	- that we meet with their team and discuss what we've learned
 - After gathering training pictures, it was discovered that the TRIMARC cameras move, changing directions to face different parts of the highway, this has large implications for training the models
 - Public KYTC server has "direction" on their listing of the info for different cameras, which could mean that we could find out what direction cameras are facing (but this needs to be tested manually by comparing the dataset and picture for a camera before and after moving)
 - set up remote access for team members access to the local server

#### Tentative Server Structure
![image](https://github.com/user-attachments/assets/16b0ce00-bde7-490d-a464-2b696becea2a)

### Actionables:
- finish gathering camera list and descriptions
- generate training images for camera list
- generate a chart of functions that govern the server and how the files will be structured


## 10/1/2024
### Updates:

#### 10/2/2024
- Met with Professor Clint Franklin in Geosciences, discussed access to public ArcGIS REST API and found solution that would reliably gather information about traffic cameras
- Met with Professor Sexton about tentative server structure. Discussed potential changes including:
	- Separating backend endpoint into the flask server
   	- Separating database from flask server
   	- Separating image processing and logic from flask server
- Essentially splitting tentative flask server structure into their own applications



### 10/8/2024
Completed:
- Finished designating scope of the project
- Finished SRS
- Met with Clint Franklin about accessing KYTC server, made progress and successfully accessed JSON data for traffic cameras
- Met with Professor Sexton and discussed the design of the local processing
- Reorganized design for local processing to split the components of our project apart into semi-independent units

#### Potential Changes:
- Proposed accessing weather data to judge conditions

#### Actionables in 2 weeks:
- John: Finish coding framework for local processing, set up database
- Mason: Finish learning about React application
- Aaron: Finish training general model and apply model on hardware


### 10/22/2024
Completed:
- Finished basic framework including main loop, database, and auxiliary programs to populate database, including the database functions used in local programs
- Finished learning about react framework, including setting up sample Vercel hosting for a webpage
- Finished training a daylight model, successfully applied model and produced results on local hardware
- Tested GPU versus CPU utilization on model and concluded that CPU may be acceptable, results pending
- Finished script to automate pulling camera information from ArcGIS server and for backing up and keeping the size of the database down

### Potential Changes:
- Emailed KYTC about data involving camera orientation and zoom level, according to them the data is inaccessible and they suggested using frame references to solve the problem

#### Actionables in 1 Week:
- Complete RF3
- John: Get main loop running with model included
- Mason: Develop the displayed webpage
- Aaron: Finish annotating the "night" dataset





#### Actionables in 2 Weeks
- John: Incorporate the night model, get the backend working on the local hardware server
- Mason: Get the website up and get a skeleton going
- Aaron: Evaluate results for nighttime model, maybe try pretrained models
