# Coffee Beans Live Detection Web Application

This project is a web-based application for detecting coffee beans' quality using YOLOv5 and Django. The application classifies coffee beans into four categories from an Live Stream:

- **Broken**
- **COCO**
- **Immature**
- **Normal**

## Features

- **Django Backend**:
  - Web-based interface to upload and analyze coffee bean images.
  
- **YOLOv5 Integration**:
  - Utilizes a pre-trained YOLOv5 model for object detection and classification.

- **Image Processing**:
  - Accepts images of coffee beans as input.
  - Outputs the classification of detected beans with bounding boxes.

- **Real-time Results**:
  - Displays the results of detection and classification directly on the web interface.

## Run the Script
### Step 1:
Clone the repository
```bash
git clone https://github.com/fahadahmedkhokhar/Coffee-Bean-Detection-using-YoloV5
```
### Step 2:
Move to the specified location.
```bash
cd Coffee-Bean-Detection-using-YoloV5/stream
```
### Step 3:
Create and activate virtual environment
```bash
conda create -n Coffee-Bean-Detection-using-YoloV5
conda activate Coffee-Bean-Detection-using-YoloV5
```
### Step 4:
Install requirements using requirements.txt
```bash
pip install -r requirement.txt
```

## Video

![Video](https://github.com/fahadahmedkhokhar/Coffee-Bean-Detection-using-YoloV5/blob/master/video.mp4)
## Report

[Documents](https://github.com/fahadahmedkhokhar/Coffee-Bean-Detection-using-YoloV5/blob/master/Report.docx) are available

