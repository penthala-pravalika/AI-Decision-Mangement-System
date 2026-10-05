# 🤖 AI Decision Management Platform

An AI Decision Management Platform built with **Python and Streamlit** to help users record, organize, review, and manage important decisions in a structured way.

## 📌 Project Overview

In organizations and project teams, many important decisions are made during meetings and discussions. It can be difficult to remember why a particular decision was made later.

This project provides a simple platform where users can:

* Create and record decisions
* Store the problem or situation
* Record available options
* Select the final decision
* Add the reason behind the decision
* Assign a decision owner
* Track decision status
* Review previous decisions
* Search decision history
* View decision statistics through a dashboard

## ✨ Features

### 📊 Dashboard

Provides an overview of:

* Total decisions
* Approved decisions
* Pending decisions
* Rejected decisions
* Recent decisions

### 📝 Create Decision

Users can record:

* Decision title
* Problem or situation
* Available options
* Selected option
* Reason for decision
* Decision owner
* Decision status

### 📚 Decision History

Users can review previously created decisions and search for decisions by title.

### ✅ Decision Status

Each decision can have one of the following statuses:

* Pending
* Approved
* Rejected

### 🔐 Data Validation

The project uses **Pydantic** models to validate decision data before storing it.

## 🛠️ Technology Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Core programming language       |
| Streamlit     | Web application interface       |
| Pydantic      | Data validation                 |
| python-dotenv | Environment variable management |
| Requests      | HTTP/API requests               |

## 📂 Project Structure

```text
AI Decision Managment/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-decision-management.git
```

### 2. Open the project

```bash
cd ai-decision-management
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

Run:

```bash
streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

## 📋 Example Decision

### Decision Title

```text
Select Database for Project
```

### Problem

```text
The project requires a reliable relational database.
```

### Available Options

```text
1. MySQL
2. PostgreSQL
3. SQLite
```

### Selected Option

```text
PostgreSQL
```

### Reason

```text
PostgreSQL provides strong relational database features,
scalability, and good support for complex queries.
```

### Status

```text
Approved
```

## 🎯 Project Objectives

The main objectives of this project are:

1. To create a centralized decision-recording system.
2. To improve decision tracking.
3. To preserve the reasoning behind decisions.
4. To make previous decisions easier to find.
5. To provide a simple dashboard for decision monitoring.
6. To create a foundation for future AI-powered decision analysis.

## 🚀 Future Enhancements

The project can be extended with:

* 🤖 AI-powered decision recommendations
* 🔍 Semantic search using embeddings
* 📚 Retrieval-Augmented Generation (RAG)
* 🧠 Similar decision detection
* 💬 AI chatbot for decision history
* 🗄️ PostgreSQL/MySQL database
* 👥 User authentication
* 🔐 Role-Based Access Control (RBAC)
* 📄 Document upload
* 📝 Meeting-notes summarization
* 📊 Advanced analytics
* 🔔 Approval notifications
* 🕒 Complete decision audit trail
* 🐳 Docker deployment
* ☁️ Cloud deployment

## 🔮 Future AI Architecture

```text
User
  ↓
Streamlit Interface
  ↓
Decision Management
  ↓
Database
  ↓
Document / Decision Retrieval
  ↓
RAG System
  ↓
AI Model
  ↓
Decision Insights
  ↓
Recommendation
```

## 🎓 Learning Outcomes

Through this project, you can learn:

* Python application development
* Streamlit UI development
* Form handling
* Session state management
* Pydantic data validation
* Environment variable management
* Git and GitHub
* Basic software project structure
* Foundations for RAG and AI applications

## 👩‍💻 Author

**Pravalika Penthala**

B.Tech Computer Science Engineering Student

## 📄 License

This project is created for educational and portfolio purposes.
