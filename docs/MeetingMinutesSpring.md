# Meeting Minutes Spring Semeester

### 1/14/2024

#### Tasks for each component:

##### Frontend:
- Schedule requests that communicate with backend
- Add additional information required on web page
- Receive coords and density from backend, store as variable
- Displays coords and density on heatmap

##### Model:
- Establish acceptable accuracy levels
- Expand datasets to meet acceptable accuracy
- Current levels, daytime 80% accuracy, nighttime 60% accuracy
- Consider other models
- Set up testing mode that stores annotated pictures in a folder for human evaluation

##### Backend:
1. Fix current configuration on server (path issue)
2. Complete auxiliary loop
3. Set up switching of models in main loop
4. Implement authentication/reverse proxy
5. Implement exceptions - outside events for failure events
6. Production ready preparation
7. Set up logging and monitoring
8. Observe operation in testing mode

- Model system as flowchart for ease of development

#### Current Changes to plans:
- Establish settings for no overlapping boxes/ no boxes within other boxes, this could possibly be done manually with the outputs of the results obtained with the model (through comparing the points of the bounding boxes)
- The labels for "cars facing with no glare" has been removed, just "car glare" and "semi" for front facing cars
- Polygons have been removed from a model, while others still need to be removed, these mess up the models as they are intended for segmentation tasks

### Current Timeline:
**January 14th-20th**:
- Backend #1,2
- Sunset/sunrise annotation/training

**January 21st-27th**:
- Backend #3
- Night-rain annotation/training

**January 28th-February 3rd**:
- Backend #4
- Night/Day snow annotation/training

**February 4th-10th**:
- Backend #5,6,7
- Model metrics and comparison to choose final configuration

**February 11th-17th**:
**Testing Begins**



Picture of meeting notes:
![20250114_170753](https://github.com/user-attachments/assets/6f9590da-b7d4-4737-b79f-8d5608c47377)
