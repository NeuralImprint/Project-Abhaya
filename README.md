# 🌸 Project Abhaya

> **Empowering Women's Health through Artificial Intelligence**

Abhaya Project is an AI-based digital healthcare application that offers comprehensive health services related to menstruation, reproduction, and psychological well-being of women. This platform integrates intelligent cycle tracking, early health risks prediction, personalized suggestions, psychological guidance, information materials, and consultation from experts within one ecosystem.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Key Features](#-features)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Future Scope](#-future-scope)

---

## Overview

Current healthcare apps for women concentrate mainly on menstrual cycle tracking without giving due consideration to other reproductive health issues such as Polycystic Ovarian Syndrome (PCOS)/Polycystic Ovary Disease (PCOD), mental well-being, healthy living tips, and consistent healthcare services.

In contrast, Project Abhaya makes up for such deficiencies with the help of various innovative technologies such as Artificial Intelligence, Machine Learning, Cloud Computing, and Digital Healthcare.

---

## Problem Statement

Millions of women experience:

- Irregular menstrual cycles
- PCOS/PCOD
- Hormonal imbalance
- Menstrual pain
- Mood disorders
- Lack of awareness
- Delayed diagnosis
- Limited healthcare accessibility

Existing healthcare applications provide only basic tracking and fail to deliver personalized, preventive, and integrated healthcare solutions.

---

## Objectives

- Promote preventive women's healthcare
- Improve awareness regarding reproductive health
- Enable early identification of menstrual disorders
- Provide AI-driven personalized recommendations
- Integrate mental wellness into menstrual healthcare
- Improve accessibility to expert consultations
- Build a secure and scalable healthcare ecosystem

---

## ✨ Features

### 🌸 Smart Menstrual Tracker
- Cycle prediction & period reminders
- Ovulation prediction & fertility window
- Cycle history & variance analysis

### 🤖 AI Health Assessment
- Personalized health questionnaire
- PCOS risk estimation with AI scoring
- AI wellness score & lifestyle recommendations

### 💬 Abhaya AI Chatbot
- Powered by Google Gemini AI
- Women's health Q&A with empathetic persona
- Period myth-busting & stress reduction guidance

### 👥 Community
- Anonymous experience sharing
- PCOS journey support
- Period awareness content & wellness stories

### 🔐 Health Vault
- Secure medical report storage
- Prescription management
- Health history tracking

### 👩‍⚕️ Expert Consultations
- Gynecologist, Nutritionist, Therapist access

---

## 📁 Project Structure

```
Project-Abhaya/
├── frontend/                    # Client-side application
│   ├── index.html               # Main HTML page
│   ├── style.css                # Complete styling
│   └── script.js                # Frontend logic + API calls
│
├── backend/                     # FastAPI backend service
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # App entry point (routers + middleware)
│   │   ├── config.py            # Settings from .env
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py       # Pydantic request/response models
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── health.py        # PCOS risk + cycle analytics
│   │   │   ├── chat.py          # Gemini AI chatbot
│   │   │   └── community.py     # Community CRUD (MongoDB)
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── analytics.py     # Cycle metrics engine
│   │       └── recommendations.py  # Phase-based wellness engine
│   ├── .env                     # Environment variables
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile               # Container config
│
├── README.md
└── .gitignore
```

---

## 🛠 Technology Stack

| Layer      | Technology                     |
|------------|-------------------------------|
| Frontend   | HTML5, CSS3, JavaScript (ES6+) |
| Backend    | Python, FastAPI, Uvicorn       |
| AI/ML      | Google Gemini AI, Scikit-learn  |
| Database   | MongoDB (Motor async driver)   |
| Deployment | Docker                         |

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- MongoDB (local or Atlas) — *optional, falls back to in-memory*
- Google Gemini API key — *for chatbot feature*

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Project-Abhaya.git
cd Project-Abhaya
```

### 2. Set Up the Backend
```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment
Edit `backend/.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=abhaya_database
```

### 4. Start the Backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 5. Open the Frontend
Open `frontend/index.html` in your browser.

---

## 📖 Usage

1. **Health Assessment**: Click "Analyze Health" → fill in symptoms → get AI risk report
2. **AI Chatbot**: Ask questions about periods, PCOS, wellness in the chat section
3. **Community**: Click category cards → read/share anonymous experiences
4. **Dashboard**: View live health score, cycle status, PCOS risk, mood analysis

---

## 📡 API Endpoints

| Method | Endpoint                          | Description                    |
|--------|-----------------------------------|--------------------------------|
| GET    | `/`                              | Health check                   |
| POST   | `/api/predict/pcos-risk`          | PCOS risk assessment           |
| POST   | `/api/chat/abhaya-bot`            | AI chatbot query               |
| POST   | `/api/analytics/cycle-summary`    | Cycle metrics & predictions    |
| POST   | `/api/analytics/recommendations`  | Phase-based recommendations    |
| GET    | `/api/community/{category}`       | Fetch community posts          |
| POST   | `/api/community/{category}/post`  | Create community post          |

Interactive API docs available at: `http://127.0.0.1:8000/docs`

---

## 🔮 Future Scope

- Mobile app (React Native / Flutter)
- Wearable device integration
- Advanced ML models for PCOS prediction
- Telemedicine video consultations
- Multi-language support
- Health data export (PDF reports)

---

## 📄 License

This project is developed for educational and healthcare awareness purposes.

---

*🌸 Built with care for women's health — Project Abhaya*
