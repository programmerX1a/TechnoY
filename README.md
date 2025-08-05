
# Technologera

**Technologera** is a beginner-friendly Flask web application that simulates an online course platform. Users can register, log in, browse available courses, join them, view transaction history, and request refunds. This project was built as an educational exercise to practice full-stack web development using Python, Flask, and SQLite.

---

## 🌐 Project Overview

Technologera replicates basic features of an e-learning platform to demonstrate concepts in backend development, web routing, session management, and dynamic front-end rendering. It includes secure login functionality, templating with Jinja2, and user-specific data handling using SQLite.

---

## 🚀 Features

- 🔐 **User Authentication**
  - Registration with password strength feedback 
  - Secure login/logout using hashed passwords and sessions
- 📚 **Course Listings**
  - View list of available courses with titles, instructors, and images
- 💳 **Join Courses**
  - Simulated course enrollment with balance deduction and Good Form formatting for the payment webpage (Luhn's Algorithm also implemented)
- 📜 **Transaction History**
  - Table showing enrolled courses and their prices with a Refund System
- 🔁 **Refund System**
  - Request refunds to return the course price to user balance

---

## ⚙️ Technologies Used

- **Python 3.13.5**
- **Flask** – Web framework
- **SQLite** – Lightweight file-based database
- **Flask-Login** – User session/authentication
- **Flask-Session** – Server-side sessions
- **zxcvbn** – Password strength checker and Password Hashing
- **HTML/CSS/JavaScript** – Frontend
- **Bootstrap** – UI responsiveness and styling

---
  ## 🖥️ Setup Instructions

Follow these steps to run the app locally:

### 1. 📦 Clone or Download

Option A – Clone via Git:
git clone https://github.com/programmerX1a/Technologera.git
cd Technologera
Option B – Download ZIP:

Click the green "Code" button on GitHub

Select "Download ZIP"

Extract the contents

### 2. 🐍 Install Dependencies
Make sure Python 3 is installed. Then run:


pip install -r requirements.txt
This installs Flask, Flask-Login, Flask-Session, zxcvbn, and more.

### 3. 🚦 Run the App
In your terminal:

Windows:

set FLASK_APP=app.py
flask run

macOS/Linux:

export FLASK_APP=app.py
flask run
Then open the given address, typically:

Then just CTRL+LEFT CLICK the port given
