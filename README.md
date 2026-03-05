# AI Expense Tracker

A personal expense tracking and analytics system built using **FastAPI, MySQL, and Streamlit**.
The application allows users to record daily expenses, categorize spending, and analyze financial patterns through a simple dashboard.

---

## Features

* Add new expenses with category and description
* View all recorded expenses
* Delete expenses
* Categorized expense tracking
* Expense analytics and visualizations
* Backend API built with FastAPI
* Interactive dashboard using Streamlit

---

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* MySQL

### Frontend

* Streamlit

### Data & Analytics

* Pandas
* NumPy
* Matplotlib
* Scikit-learn

### Other Tools

* Uvicorn
* Requests

---

## Project Structure

AI-Expense-Tracker

backend/
    routes/
    models/
    main.py

frontend/
    streamlit_app.py

analytics/
    expense_analysis.py

database/

requirements.txt
README.md

---

## How to Run the Project

### 1. Clone the repository

git clone https://github.com/your-username/ai-expense-tracker.git
cd ai-expense-tracker

### 2. Install dependencies

pip install -r requirements.txt

### 3. Run the FastAPI backend

uvicorn backend.main:app --reload

### 4. Run the Streamlit frontend

streamlit run frontend/streamlit_app.py

---

## Future Improvements

* Budget tracking system
* Monthly spending analytics
* Expense prediction using machine learning
* Improved dashboard UI

---

## Author

Tejaa
Computer Science Student
