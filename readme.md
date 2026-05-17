# AI Travel Planner System

An intelligent AI-powered travel planning and tourism management system built using Flask, MySQL, Machine Learning, Geoapify APIs, OpenWeather APIs, and dynamic scheduling algorithms.

---

# Features

- AI-based Travel Schedule Generation
- Dynamic Trip Planner
- Budget Management System
- Hotel Recommendation System
- Nearby Restaurants & Hotels
- Weather Integration
- Smart Route Finder
- Geoapify Location Services
- Reverse Geocoding
- Sentiment Analysis on Hotel Reviews
- Tourist Place Suggestions
- Authentication System
- ML-based Recommendation Models

---

# Technologies Used

## Backend
- Flask
- Flask-MySQLdb
- Flask-CORS
- Python

## Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

## Database
- MySQL

## APIs
- Geoapify API
- OpenWeather API
- SerpAPI

## Machine Learning
- Scikit-learn
- Joblib
- NumPy
- Pandas

---

# Project Structure

```bash
Major_Project/
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── models/
│   ├── templates/
│   └── static/
│
├── data/
├── ml_models/
├── config.py
├── run.py
├── requirements.txt
├── .env
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <your_repository_url>
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory.

Example:

```env
SECRET_KEY=your_secret_key

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=Users

GEOAPIFY_KEY=your_geoapify_key
OPENWEATHER_KEY=your_openweather_key
SERPAPI_API_KEY=your_serpapi_key
```

---

# Running the Project

```bash
python run.py
```

---

# Production Deployment

## Gunicorn

```bash
gunicorn run:app
```

---

# Main Modules

- Authentication Module
- Travel Planner
- Dynamic Scheduler
- Hotel Review Analyzer
- Route Finder
- Budget Planner
- Tourism Recommendation Engine

---

# APIs Used

## Geoapify
- Geocoding
- Reverse Geocoding
- Places API
- Routing API

## OpenWeather
- Current Weather API

## SerpAPI
- Google Maps Reviews API

---

# Future Improvements

- JWT Authentication
- Docker Support
- Redis Cache
- AI Chatbot Integration
- PDF Report Generation
- Email Notifications
- Cloud Deployment
- Mobile Application

---

# Author

Gursimran Kaur

---