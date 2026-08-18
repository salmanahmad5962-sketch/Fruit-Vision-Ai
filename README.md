# 🍎 Fruit Vision AI

An AI-powered fruit classification platform that identifies fruits from uploaded images and provides prediction results, confidence scores and nutritional information through a modern web interface.

The project combines **Artificial Intelligence, Computer Vision, Flask and SQLite** to create a practical fruit recognition system.

## 🌐 Live Demo

**[Try Fruit Vision AI](https://fruit-vision-ai.onrender.com)**

## ✨ Features

* 🤖 AI-powered fruit classification
* 📷 Image-based fruit recognition
* 🎯 Prediction results
* 📊 Confidence scores
* 🍎 Fruit health and nutrition information
* 🔥 Flask backend
* 🗃️ SQLite database
* 👤 User authentication
* 📋 Image checking history
* 👑 Admin functionality
* 🖼️ Uploaded image management
* 📱 Responsive web interface
* 🔌 REST API
* ❤️ Health-check endpoint
* 📦 Progressive Web App support

## 🧠 AI Model

The application uses a **Hugging Face-compatible ResNet-based fruit classification model** to process uploaded fruit images and generate predictions.

The model pipeline is integrated with the Flask backend and exposed through an API.

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* SQLite
* REST API

### AI / Machine Learning

* ResNet
* Hugging Face-compatible model
* Computer Vision
* Image Classification

### Frontend

* HTML5
* CSS3
* JavaScript
* Responsive UI

### Other

* Service Worker
* PWA Manifest
* Render deployment

## 📁 Project Structure

```text
Fruit-Vision-Ai/
├── assets/
├── models/
├── uploads/
├── app.py
├── Fruit Classification.html
├── auth.html
├── fruit_health_info.py
├── fruitai.db
├── manifest.json
├── render.yaml
├── requirements.txt
├── service-worker.js
├── .gitignore
└── README.md
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/salman-devX/Fruit-Vision-Ai.git
cd Fruit-Vision-Ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5001
```

## 🔌 API Endpoints

### Predict Fruit

```text
POST /api/predict
```

Accepts an image and returns the predicted fruit information.

### Health Check

```text
GET /api/health
```

Used to verify that the backend service is running correctly.

## 🗃️ Data & History

The application uses SQLite for persistence and can maintain information related to checked images.

Uploaded images are stored in the `uploads/` directory and can be accessed through the application's administrative functionality.

## 🍎 Nutrition Information

Fruit information can include nutritional and health-related details such as calorie information and other available fruit insights.

## 🎯 Project Objective

Fruit Vision AI was developed to demonstrate how artificial intelligence and computer vision can be integrated into a practical web application.

The system provides an easy-to-use interface where users can upload a fruit image and receive an AI-generated classification result.

## 🚀 Deployment

The project is configured for deployment using **Render**.

### Live Application

https://fruit-vision-ai.onrender.com

## 🔮 Future Improvements

* Support for more fruit categories
* Improved model accuracy
* Mobile application
* Advanced nutrition analytics
* User-specific prediction history
* Enhanced admin dashboard
* Cloud image storage
* Model performance monitoring
* Multi-language support

## 👨‍💻 Developer

**Salman Ahmad**

Web Developer • Software Developer • AI/ML Enthusiast

## 🔗 Links

* 🌐 Live Website: https://fruit-vision-ai.onrender.com
* 🐙 GitHub: https://github.com/salman-devX

## 📄 License

This project is created and maintained by Salman Ahmad.
