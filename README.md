# 🤖 AI Decision Management System

An **AI-powered Decision Management System** built with **Python, Streamlit, and Gemini AI**.

The system helps employees create business/project decisions, receive AI-powered suggestions and risk analysis, and submit decisions to a manager for final approval or rejection.

---

## 📌 Project Overview

In organizations, employees often need to make decisions related to projects, technologies, databases, tools, and business processes.

This project provides a centralized platform where:

* Employees can create decisions.
* Gemini AI analyzes the decision.
* AI provides suggestions, risks, and recommendations.
* Employees submit decisions to managers.
* Managers review the decisions.
* Managers can approve or reject decisions.
* Employees can track the final decision status.

The system demonstrates how **Generative AI can support organizational decision-making while keeping humans responsible for the final decision.**

---

## 🎯 Objectives

The main objectives of this project are:

1. Provide a simple platform for managing organizational decisions.
2. Use Gemini AI to analyze decision options.
3. Identify potential risks before making a decision.
4. Allow employees to submit decisions to managers.
5. Allow managers to approve or reject decisions.
6. Maintain decision history.
7. Provide transparency between employees and managers.
8. Demonstrate Human-in-the-Loop AI decision making.

---

## ✨ Features

### 👨‍💻 Employee Features

* Employee login
* Create new decisions
* Enter decision description
* Add multiple decision options
* Generate AI analysis
* View AI suggestion
* View risk analysis
* View AI recommendation
* Submit decision to manager
* Track decision status
* View manager comments

### 👨‍💼 Manager Features

* Manager login
* View employee decisions
* View AI analysis
* View pending decisions
* Approve decisions
* Reject decisions
* Add manager comments
* View previously reviewed decisions

### 🤖 AI Features

Gemini AI provides:

* AI Suggestion
* Risk Analysis
* Final Recommendation

The AI only provides **decision support**. The manager makes the final approval or rejection.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       Employee       │
                    │        Login         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Create Decision    │
                    │ Title / Description  │
                    │      / Options       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Gemini AI       │
                    │                      │
                    │ • AI Suggestion      │
                    │ • Risk Analysis      │
                    │ • Recommendation     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Submit to Manager    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    decisions.json    │
                    │   Decision Storage   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Manager        │
                    │        Login         │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌─────────────┐       ┌─────────────┐
             │   Approve   │       │   Reject    │
             └──────┬──────┘       └──────┬──────┘
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌──────────────────────┐
                    │   Final Status       │
                    │ Approved / Rejected  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Employee Views Result│
                    └──────────────────────┘
```

---

## 🛠️ Technologies Used

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Application development         |
| Streamlit     | Web application interface       |
| Gemini AI     | AI decision analysis            |
| Requests      | Gemini REST API communication   |
| Pydantic      | Data validation                 |
| python-dotenv | Environment variable management |
| JSON          | Local decision storage          |

---

## 📁 Project Structure

```text
AI Decision Management/
│
├── app.py
├── decisions.json
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Requirements

Make sure Python is installed.

Recommended Python version:

```text
Python 3.12.x
```

---

## 📦 Installation

### 1. Clone or create the project

Open PowerShell:

```powershell
cd "C:\Users\penth\Desktop"
```

Create/open the project folder:

```powershell
cd "AI Decision Management"
```

---

### 2. Create a virtual environment

```powershell
python -m venv venv
```

---

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\activate
```

If PowerShell blocks activation, you can run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\venv\Scripts\activate
```

---

## 📦 Install Dependencies

Run:

```powershell
pip install -r requirements.txt
```

The project uses:

```text
streamlit==1.40.1
python-dotenv==1.0.1
requests==2.32.3
pydantic==2.10.3
```

---

## 🔑 Gemini API Key Setup

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do **not** upload the `.env` file to GitHub.

The application reads the API key using:

```python
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

---

## 🔐 Demo Login Credentials

### Employee

```text
Username: employee1
Password: employee123
```

Second employee:

```text
Username: employee2
Password: employee123
```

### Manager

```text
Username: manager1
Password: manager123
```

These are demo credentials for the prototype.

---

## ▶️ Run the Application

Start Streamlit:

```powershell
streamlit run app.py
```

The application will open in your browser.

Usually:

```text
http://localhost:8501
```

---

# 🧑‍💻 How the System Works

## Step 1 — Employee Login

The employee enters:

```text
Username
Password
```

After successful authentication, the employee dashboard is displayed.

---

## Step 2 — Create Decision

The employee enters:

```text
Decision Title
Decision Description
Available Options
```

Example:

```text
Decision Title:
Choose Database for AI Project
```

Description:

```text
Our team is developing an AI Decision Management
System. We need a database that is reliable,
secure, scalable, and suitable for structured data.
```

Options:

```text
Option A: MySQL
Option B: PostgreSQL
Option C: MongoDB
```

---

## Step 3 — AI Analysis

The employee clicks:

```text
Get Gemini AI Suggestion
```

Gemini analyzes the decision.

The system displays:

### AI Suggestion

Provides a practical suggestion based on the available options.

### Risk Analysis

Identifies:

* Technical risks
* Cost risks
* Scalability risks
* Security concerns
* Maintenance concerns

### AI Recommendation

Provides a recommended option with reasoning.

---

## Step 4 — Submit to Manager

After reviewing the AI analysis, the employee clicks:

```text
Submit Decision to Manager
```

The decision is stored in:

```text
decisions.json
```

Its status becomes:

```text
Pending
```

---

## Step 5 — Manager Login

The manager logs in using:

```text
Username: manager1
Password: manager123
```

The manager can see all employee decisions.

---

## Step 6 — Manager Review

The manager can view:

* Employee name
* Decision title
* Description
* Available options
* AI suggestion
* Risk analysis
* AI recommendation

The manager can enter a comment.

---

## Step 7 — Manager Decision

The manager has two choices:

```text
✅ Approve Decision
```

or

```text
❌ Reject Decision
```

If approved:

```text
Status = Approved
```

If rejected:

```text
Status = Rejected
```

---

## Step 8 — Employee Checks Status

The employee logs in again and opens:

```text
My Decisions
```

The employee can see:

```text
Approved
```

or:

```text
Rejected
```

along with the manager's comment.

---

# 📊 Decision Status

The system supports three main statuses:

```text
Pending
Approved
Rejected
```

### Pending

The decision is waiting for manager review.

### Approved

The manager has accepted the decision.

### Rejected

The manager has rejected the decision.

---

# 💾 Data Storage

The prototype uses:

```text
decisions.json
```

Example:

```json
[
    {
        "id": 1,
        "employee": "employee1",
        "title": "Choose Database",
        "description": "Select a database for the project.",
        "options": "MySQL, PostgreSQL, MongoDB",
        "ai_suggestion": "PostgreSQL is a strong choice.",
        "ai_risk": "Consider cost and maintenance.",
        "ai_recommendation": "PostgreSQL is recommended.",
        "status": "Pending",
        "manager_comment": "",
        "created_at": "2026-10-05 16:30:00",
        "reviewed_at": ""
    }
]
```

---

# 🔒 Security

The project follows basic security practices for a prototype.

### API Key Protection

The Gemini API key is stored in:

```text
.env
```

The `.env` file should not be committed to GitHub.

### Git Ignore

The project includes:

```text
.env
venv/
__pycache__/
decisions.json
```

---

# 🧪 Example Use Cases

The system can be used for decisions such as:

### Database Selection

```text
MySQL
PostgreSQL
MongoDB
```

### Programming Language Selection

```text
Python
Java
JavaScript
```

### Cloud Platform Selection

```text
AWS
Azure
Google Cloud
```

### Project Management Tool

```text
Jira
Trello
Excel
```

### Hardware Selection

```text
8 GB RAM
16 GB RAM
32 GB RAM
```

---

# 🎯 Advantages

* Simple and user-friendly interface
* AI-assisted decision analysis
* Human-in-the-loop decision making
* Manager approval workflow
* Risk analysis before approval
* Centralized decision history
* Employee and manager separation
* Easy to demonstrate
* Suitable for an academic project prototype

---

# 🚀 Future Enhancements

The current system is a prototype. Future versions can include:

1. **Database Integration**

   * MySQL
   * PostgreSQL
   * MongoDB

2. **Advanced Authentication**

   * Secure password hashing
   * JWT authentication
   * Role-Based Access Control

3. **More User Roles**

   * Employee
   * Reviewer
   * Manager
   * Administrator

4. **Decision Versioning**

   * Track changes to decisions
   * Compare previous versions

5. **Audit Logs**

   * Record who created a decision
   * Record who approved/rejected it
   * Store timestamps

6. **Document Upload**

   * Upload project documents
   * Analyze supporting documents using AI

7. **Advanced AI**

   * Decision confidence scoring
   * Alternative generation
   * Impact analysis
   * Cost-benefit analysis

8. **Analytics Dashboard**

   * Total decisions
   * Approval rate
   * Rejection rate
   * Pending decisions
   * Department-wise statistics

9. **Notifications**

   * Email notifications
   * Manager alerts
   * Employee status notifications

10. **Cloud Deployment**

    * Streamlit Cloud
    * AWS
    * Azure
    * Google Cloud

---

# ⚠️ Limitations

This version is intended as an academic prototype.

* User accounts are
