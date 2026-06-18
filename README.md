# 🚀 AI Resume Analyzer & Career Assistant

An AI-powered Resume Analysis and Career Guidance platform that helps students and job seekers identify suitable career paths, discover skill gaps, and receive personalized learning recommendations.

Built with **Python, FastAPI, LangChain, Groq API, and ChromaDB**, the system combines Resume Parsing, Skill Analysis, Career Recommendation, Retrieval-Augmented Generation (RAG), and an AI Career Assistant Chatbot.

---


<h2>📸 Project Preview</h2>

<h3>🏠 Home Page & Resume Upload</h3>
<img src="Screenshot 2026-06-18 133519.png" alt="Home Page" width="900">

<h3>📊 Resume Analysis</h3>
<img src="Screenshot 2026-06-18 133538.png" alt="Resume Analysis" width="900">

<h3>🎯 Skill Gap Analysis</h3>
<img src="screenshots/recommendation.png" alt="Skill Gap Analysis" width="900">

<h3>🛣 Career Roadmap</h3>
<img src="screenshots/roadmap.png" alt="Career Roadmap" width="900">

<h3>💬 AI Career Assistant Chatbot</h3>
<img src="screenshots/chatbot.png" alt="Career Assistant" width="900">

## 🎯 Problem Statement

Many students and fresh graduates struggle to understand:

* Which career path suits their skills
* What skills they are missing
* How to create a structured learning plan
* How to prepare for industry requirements

This project addresses these challenges through AI-driven resume analysis and career guidance.

---

## ✨ Features

### 📄 Resume Parsing

* Upload PDF or DOCX resumes
* Extract resume content automatically
* Process candidate information efficiently

### 🤖 AI Skill Extraction

Uses Groq LLM to identify:

* Name
* Contact Information
* Education
* Technical Skills
* Certifications

### 🎯 Career Recommendation

* Matches skills against industry role requirements
* Recommends Top 3 suitable job roles
* Calculates role match scores

### 📊 Skill Gap Analysis

* Compares current skills with required skills
* Highlights missing competencies
* Provides actionable learning suggestions

### 🛣 Personalized Career Roadmap

* Generates role-specific learning paths
* Suggests technologies and certifications
* Provides structured career growth plans

### 💬 AI Career Assistant

* RAG-powered chatbot
* Answers career-related questions
* Provides personalized guidance and recommendations

---

## 🏗 System Architecture

```text
Resume Upload
      │
      ▼
Resume Parser
      │
      ▼
Groq LLM Skill Extraction
      │
      ▼
Role Matching Engine
      │
      ▼
Skill Gap Analysis
      │
      ▼
Career Roadmap Generator
      │
      ▼
RAG-Based Career Assistant
```

---

## 🛠 Tech Stack

### Backend

* Python
* FastAPI

### AI & Machine Learning

* Groq API
* LangChain
* Retrieval-Augmented Generation (RAG)

### Vector Database

* ChromaDB

### Frontend

* HTML
* CSS
* JavaScript

### Document Processing

* PyPDF2
* python-docx

---

## 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── resume_parser.py
├── skill_extractor.py
├── role_matcher.py
├── rag_pipeline.py
├── chatbot.py
│
├── career_dataset.csv
├── career_knowledge_base.txt
├── chroma_db/
│
├── requirements.txt
├── README.md
│
└── static/
    ├── index.html
    ├── analysis.html
    ├── chat.html
    ├── css/
    └── js/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository-url>
cd AI-Resume-Analyzer
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
```

### Run Application

```bash
python app.py
```

Application runs at:

```text
http://localhost:8000
```

---

## 📈 Key Skills Demonstrated

* Generative AI
* Large Language Models (LLMs)
* Retrieval-Augmented Generation (RAG)
* Vector Databases
* LangChain Framework
* FastAPI Development
* NLP & Information Extraction
* Resume Parsing
* Backend API Development
* AI Chatbot Development

---

## 🚀 Future Enhancements

* ATS Score Prediction
* Resume Improvement Suggestions
* Interview Question Generator
* LinkedIn Profile Analysis
* Job Recommendation Engine
* Multi-language Resume Support

---

## 👨‍💻 Author

### Gunal Christ

B.Tech Artificial Intelligence & Machine Learning

**Skills:** Python • FastAPI • LangChain • Groq API • ChromaDB • RAG • NLP • Machine Learning

GitHub: https://github.com/Gunalchrist23
#
