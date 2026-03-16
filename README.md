⚡ AI Electricity Bill Predictor

Predict monthly electricity bills using Artificial Neural Networks (ANN) with a modern web interface.

A smart web application that estimates electricity bills based on TNEB tariff rates using a trained Artificial Neural Network model.
The project combines Machine Learning + FastAPI + Modern Web Development to create an intelligent electricity bill prediction system.

🚀 Live Demo (Optional)

Add this later if you deploy the project.

Demo Link: Coming Soon
📌 Project Overview

Electricity bill calculation can be complex due to changing tariff slabs and usage patterns.

This project solves that by using an ANN model trained on electricity consumption patterns to predict electricity bills efficiently.

The system includes:

• AI model for bill prediction
• FastAPI backend for inference
• Modern responsive frontend
• Progressive Web App (PWA) support
• Docker containerization

This makes the application fast, scalable, and easy to deploy.

✨ Features

✅ AI-based electricity bill prediction
✅ FastAPI high-performance backend
✅ Responsive modern frontend
✅ Progressive Web App (Installable App)
✅ Offline caching using Service Worker
✅ Dockerized backend for easy deployment
✅ Supports Tamil Nadu Electricity Board (TNEB) tariff system

🧠 AI Model

The electricity bill prediction is powered by a trained Artificial Neural Network (ANN).

Model Inputs

Electricity units consumed

Tariff slab ranges

TNEB billing rules

Model Output

Estimated electricity bill

Libraries used:

TensorFlow / Keras

Joblib

NumPy

Scikit-learn

🛠 Tech Stack
Backend

Python

FastAPI

TensorFlow / Keras

Joblib

Frontend

HTML

CSS

JavaScript

Deployment

Docker

PWA (Service Worker)

📂 Project Structure
ai-electricity-bill-predictor
│
├── backend
│   ├── Dockerfile
│   ├── main.py
│   ├── model.h5
│   ├── scaler.save
│   ├── y_scaler.save
│   └── requirements.txt
│
├── frontend
│   ├── index.html
│   ├── manifest.json
│   ├── sw.js
│   └── icon/
│
├── .gitignore
├── LICENSE
└── README.md
⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/eswaran200dsu/ai-electricity-bill-predictor.git
cd ai-electricity-bill-predictor
🖥 Backend Setup
Option 1 — Docker (Recommended)
cd backend
docker build -t electricity-bill-backend .
docker run -p 7860:7860 electricity-bill-backend
Option 2 — Local Setup
cd backend
python -m venv venv

Activate environment

Windows

venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Run FastAPI server

uvicorn main:app --host 0.0.0.0 --port 7860
🌐 Frontend Setup

Open the frontend directly in browser

frontend/index.html

Or serve it using any static server.

📖 How It Works

1️⃣ User enters electricity consumption
2️⃣ Frontend sends request to FastAPI API
3️⃣ ANN model processes the input
4️⃣ Predicted electricity bill is returned
5️⃣ Frontend displays the estimated bill

📱 Progressive Web App

This project supports PWA installation.

Users can:

✔ Install the app
✔ Use offline caching
✔ Get faster loading

🤝 Contributing

Contributions are welcome!

Steps:

1️⃣ Fork the repository
2️⃣ Create a feature branch

git checkout -b feature-name

3️⃣ Commit changes

git commit -m "Add feature"

4️⃣ Push branch

git push origin feature-name

5️⃣ Open Pull Request

📜 License

This project is licensed under the MIT License.

👨‍💻 Author

Eswaran

AI & Data Science Student
Passionate about Machine Learning, AI Applications, and Data Science

GitHub
https://github.com/eswaran200dsu

⭐ Support

If you found this project helpful:

⭐ Star the repository
🍴 Fork the project
📢 Share with others

🔥 Result

This README now has:

✅ Professional structure
✅ Recruiter-friendly explanation
✅ Clean sections
✅ AI model explanation
✅ Project workflow
