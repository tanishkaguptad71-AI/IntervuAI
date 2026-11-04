IntervuAI – AI Mock Interview System

An interactive mock interview platform designed to help students and job seekers practice technical interviews, evaluate their answers, and improve their interview performance.

About the Project

IntervuAI is a Python-based mock interview application that provides a structured interview experience. Users can select their preferred job role and difficulty level, answer interview questions, and receive question-wise feedback with a performance report.

Key Features

- Candidate registration
- Multiple job roles
- Beginner, Intermediate and Advanced difficulty levels
- Five questions per interview
- 10 marks per question (50 marks total)
- Timed interview experience
- Answer evaluation and feedback
- Performance dashboard
- Downloadable PDF interview report

Technology Stack

Technology| Purpose
Python| Core programming language
Streamlit| User interface
ReportLab| PDF report generation
Rule-based evaluation| Answer assessment and scoring

Supported Interview Roles

- AI/ML Engineer
- Python Developer
- Software Engineer
- Web Developer

Interview Process

1. Register as a candidate.
2. Select your desired job role.
3. Choose the difficulty level.
4. Start the mock interview.
5. Answer five interview questions.
6. Receive marks and question-wise feedback.
7. View your performance report.
8. Download your PDF report.

Project Structure

IntervuAI/
│
├── app.py
├── interview.py
├── ml_model.py
├── app_backup.py
└── README.md

Installation and Setup

1. Clone the repository

git clone https://github.com/tanishkaguptad71-AI/IntervuAI.git

2. Open the project folder

cd IntervuAI

3. Install dependencies

py -m pip install streamlit reportlab

4. Run the application

py -m streamlit run app.py

5. Open in your browser

The application will open at:

http://localhost:8501

Evaluation Method

The current evaluation system uses rule-based keyword matching and answer-length checks to assess responses and generate scores and feedback.

Project Objective

The main objective of IntervuAI is to provide students with an accessible platform to practice interviews, identify areas for improvement, and build confidence before real-world interviews.

Future Enhancements

- Advanced NLP-based answer evaluation
- LLM-powered personalized feedback
- Speech recognition for voice interviews
- Resume-based interview questions
- Detailed performance analytics

Project Information

Project Name: IntervuAI

Category: Artificial Intelligence / Interview Preparation

Programming Language: Python

Interface: Streamlit

Repository: https://github.com/tanishkaguptad71-AI/IntervuAI


IntervuAI – Practice Smart. Interview Better.
