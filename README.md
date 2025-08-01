# 🛰️ Satellite Water Segmentation
A deep learning web application to segment water bodies from satellite imagery using multispectral and optical data.

---

## 🧠 Overview

This project applies deep learning models (like U-Net and its variants) to perform semantic segmentation on satellite images. The goal is to accurately detect water regions from multi-band input images (e.g., 12-band Sentinel-2 imagery) and deploy the solution using a Flask web interface.

---

## 🚀 Features
- U-Net-based architecture with various backbones (ResNet34, ResNet50, EfficientNetV2B0).
- Accepts 12-channel multispectral input data.
- Pixel-wise segmentation output with water masks.
- Flask-powered web app for uploading images and displaying results.
- Evaluation metrics: Accuracy, IoU, Precision, Recall.
- Download predicted mask as an image.

---

## 📊 Dataset Summary

The dataset includes preprocessed satellite images with 12 spectral bands and corresponding binary masks indicating water bodies.

### Band Explanation

The multi-band structure enhances water segmentation accuracy.

> 📷 _Below is a sample visualization of the spectral bands:_

![Bands Explanation](Deployment/static/channels.jpg)

|Band|Min|Max|
|:----:|:---:|:---:|
|Band 1|-1393.0|6568.0|
|Band 2|-1169.0|9659.0|
|Band 3|-722.0|11368.0|
|Band 4|-684.0|12041.0|
|Band 5|-412.0|15841.0|
|Band 6|-335.0|15252.0|
|Band 7|-258.0|14647.0|
|Band 8|64.0|255.0|
|Band 9|-9999.0|4245.0|
|Band 10|8.0|4287.0|
|Band 11|10.0|100.0|
|Band 12|0.0|111.0|

---

## 🛠 Installation & Setup
```
git clone https://github.com/bassantsherif123/ComputerVision_Satellite_Image_Water_Segmentation.git
```
## 🌐 Flask App
- Upload multispectral image (with 12 channels)
- Visualize band combinations
- View the predicted segmentation mask
- Download the output mask
- Download the model using the following link, then put it to Model folder: 📥 [Download Model File](https://drive.google.com/file/d/1DHjVIwiL3VdNSP67QV9zuipDwdiQKeTz/view?usp=sharing)
### To run the app, use:
```
python Deployment/app.py
```
## 📈 Model Evaluation

| Model Name        | Accuracy | IoU  |
|:-----------------:|:--------:|:----:|
| Custom UNet       | 0.955315 | 0.826221 |
| EfficientNetV2B0  | 0.901890 | 0.408989 |
| ResNet34          | 0.958784 | 0.836132 |
| ResNet50          | 0.857304 | 0.408989|