import os
import json
from datetime import datetime

import requests
import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Force the latest model mentioned by your Gemini API
GEMINI_MODEL = "gemini-3.8-flash"

DATA_FILE = "decisions.json"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Decision Management",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# DECISION MODEL
# ============================================================

class Decision(BaseModel):
    id: int
    employee: str
    title: str
    description: str
    options: str

    ai_suggestion: str = ""
    ai_risk: str = ""
    ai_recommendation: str = ""

    status: str = "Pending"

    manager_comment: str = ""

    created_at: str = ""

    reviewed_at: str = ""


# ============================================================
# USERS
# ============================================================

USERS = {

    "employee1": {
        "password": "employee123",
        "role": "Employee",
        "name": "Employee One"
    },

    "employee2": {
        "password": "employee123",
        "role": "Employee",
        "name": "Employee Two"
    },

    "manager1": {
        "password": "manager123",
        "role": "Manager",
        "name": "Manager One"
    }
}


# ============================================================
# LOAD DECISIONS
# ============================================================

def load_decisions():

    if not os.path.exists(DATA_FILE):
        return []

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except json.JSONDecodeError:

        return []

    except Exception:

        return []


# ============================================================
# SAVE DECISIONS
# ============================================================

def save_decisions(decisions):

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            decisions,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# GEMINI AI FUNCTION
# ============================================================

def get_ai_suggestion(
    title,
    description,
    options
):

    # --------------------------------------------------------
    # Check API key
    # --------------------------------------------------------

    if not GEMINI_API_KEY:

        return (
            "Gemini API key is missing.",
            "Risk analysis unavailable.",
            "Please add GEMINI_API_KEY to your .env file."
        )

    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = f"""
You are an AI Decision Management Assistant.

Your job is to provide decision support to an employee.
The manager will make the final approval or rejection.

Analyze this decision:

DECISION TITLE:
{title}

DECISION DESCRIPTION:
{description}

AVAILABLE OPTIONS:
{options}

Return EXACTLY these three sections:

1. AI SUGGESTION
Give a practical and clear suggestion.

2. RISK ANALYSIS
Explain the major risks, disadvantages,
dependencies, and possible problems.

3. FINAL RECOMMENDATION
Recommend the best option and explain why.

IMPORTANT:
- Do not approve or reject the decision.
- Do not pretend to be the manager.
- The manager makes the final decision.
- Be professional and concise.
"""

    # --------------------------------------------------------
    # Gemini Interactions API
    # --------------------------------------------------------

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/interactions"
    )

    headers = {

        "Content-Type": "application/json",

        "x-goog-api-key": GEMINI_API_KEY
    }

    payload = {

        "model": GEMINI_MODEL,

        "input": prompt
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        # ----------------------------------------------------
        # API ERROR
        # ----------------------------------------------------

        if response.status_code != 200:

            try:

                error_data = response.json()

                error_message = (
                    error_data
                    .get("error", {})
                    .get(
                        "message",
                        response.text
                    )
                )

            except Exception:

                error_message = response.text

            return (
                f"Gemini API Error: {error_message}",
                "Risk analysis unavailable.",
                "AI recommendation unavailable."
            )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        data = response.json()

        ai_text = ""

        # Google's Interactions API response contains
        # output steps. Extract text from them.
        steps = data.get(
            "steps",
            []
        )

        for step in steps:

            content = step.get(
                "content",
                []
            )

            if isinstance(content, list):

                for item in content:

                    if isinstance(item, dict):

                        if item.get("type") == "text":

                            ai_text += (
                                item.get(
                                    "text",
                                    ""
                                )
                            )

                        elif "text" in item:

                            ai_text += (
                                item.get(
                                    "text",
                                    ""
                                )
                            )

        # ----------------------------------------------------
        # Alternative output format
        # ----------------------------------------------------

        if not ai_text:

            output = data.get(
                "output",
                []
            )

            if isinstance(output, list):

                for item in output:

                    if isinstance(item, dict):

                        if item.get("type") == "text":

                            ai_text += (
                                item.get(
                                    "text",
                                    ""
                                )
                            )

                        content = item.get(
                            "content",
                            []
                        )

                        if isinstance(
                            content,
                            list
                        ):

                            for content_item in content:

                                if isinstance(
                                    content_item,
                                    dict
                                ):

                                    if (
                                        content_item.get(
                                            "type"
                                        )
                                        == "text"
                                    ):

                                        ai_text += (
                                            content_item.get(
                                                "text",
                                                ""
                                            )
                                        )

        # ----------------------------------------------------
        # No response
        # ----------------------------------------------------

        if not ai_text:

            return (
                "Gemini returned an empty response.",
                "Risk analysis unavailable.",
                "AI recommendation unavailable."
            )

        ai_text = ai_text.strip()

        # ----------------------------------------------------
        # Separate AI sections
        # ----------------------------------------------------

        suggestion = ""
        risk = ""
        recommendation = ""

        # Normalize headings
        normalized = ai_text.replace(
            "**",
            ""
        )

        # Try to find sections
        suggestion_markers = [
            "1. AI SUGGESTION",
            "1. AI Suggestion"
        ]

        risk_markers = [
            "2. RISK ANALYSIS",
            "2. Risk Analysis"
        ]

        recommendation_markers = [
            "3. FINAL RECOMMENDATION",
            "3. Final Recommendation"
        ]

        suggestion_position = -1

        for marker in suggestion_markers:

            position = normalized.find(marker)

            if position != -1:

                suggestion_position = position

                break

        risk_position = -1

        for marker in risk_markers:

            position = normalized.find(marker)

            if position != -1:

                risk_position = position

                break

        recommendation_position = -1

        for marker in recommendation_markers:

            position = normalized.find(marker)

            if position != -1:

                recommendation_position = position

                break

        # ----------------------------------------------------
        # Extract suggestion
        # ----------------------------------------------------

        if suggestion_position != -1:

            start = (
                suggestion_position
                + len("1. AI SUGGESTION")
            )

            if risk_position != -1:

                suggestion = normalized[
                    start:risk_position
                ].strip()

            else:

                suggestion = normalized[
                    start:
                ].strip()

        # ----------------------------------------------------
        # Extract risk
        # ----------------------------------------------------

        if risk_position != -1:

            start = (
                risk_position
                + len("2. RISK ANALYSIS")
            )

            if recommendation_position != -1:

                risk = normalized[
                    start:recommendation_position
                ].strip()

            else:

                risk = normalized[
                    start:
                ].strip()

        # ----------------------------------------------------
        # Extract recommendation
        # ----------------------------------------------------

        if recommendation_position != -1:

            start = (
                recommendation_position
                + len("3. FINAL RECOMMENDATION")
            )

            recommendation = normalized[
                start:
            ].strip()

        # ----------------------------------------------------
        # Fallback
        # ----------------------------------------------------

        if not suggestion:

            suggestion = ai_text

        if not risk:

            risk = (
                "See the complete AI analysis above."
            )

        if not recommendation:

            recommendation = ai_text

        return (
            suggestion,
            risk,
            recommendation
        )

    # --------------------------------------------------------
    # TIMEOUT
    # --------------------------------------------------------

    except requests.exceptions.Timeout:

        return (
            "Gemini request timed out.",
            "Risk analysis unavailable.",
            "Please try again."
        )

    # --------------------------------------------------------
    # NETWORK ERROR
    # --------------------------------------------------------

    except requests.exceptions.RequestException as e:

        return (
            f"Network error: {e}",
            "Risk analysis unavailable.",
            "Please try again."
        )

    # --------------------------------------------------------
    # OTHER ERROR
    # --------------------------------------------------------

    except Exception as e:

        return (
            f"Unexpected error: {e}",
            "Risk analysis unavailable.",
            "Recommendation unavailable."
        )


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.title(
        "🤖 AI Decision Management"
    )

    st.subheader(
        "Login"
    )

    username = st.text_input(
        "Username",
        placeholder="Enter username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    if st.button(
        "🔐 Login",
        use_container_width=True
    ):

        username = username.strip()

        if username not in USERS:

            st.error(
                "User not found."
            )

            st.info(
                "Test users: employee1 or manager1"
            )

            return

        user = USERS[username]

        if password != user["password"]:

            st.error(
                "Incorrect password."
            )

            return

        # ----------------------------------------------------
        # Login successful
        # ----------------------------------------------------

        st.session_state.logged_in = True

        st.session_state.username = username

        st.session_state.role = user["role"]

        st.session_state.name = user["name"]

        st.success(
            "Login successful!"
        )

        st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

def sidebar():

    st.sidebar.title(
        "🤖 AI Decision Management"
    )

    st.sidebar.write(
        f"👤 {st.session_state.name}"
    )

    st.sidebar.write(
        f"Role: **{st.session_state.role}**"
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.clear()

        st.rerun()


# ============================================================
# EMPLOYEE DASHBOARD
# ============================================================

def employee_dashboard():

    st.title(
        "👨‍💻 Employee Dashboard"
    )

    st.write(
        "Create a decision and get AI-powered "
        "decision support before manager review."
    )

    create_tab, decisions_tab = st.tabs(
        [
            "➕ Create Decision",
            "📋 My Decisions"
        ]
    )

    # ========================================================
    # CREATE DECISION
    # ========================================================

    with create_tab:

        st.subheader(
            "Create New Decision"
        )

        title = st.text_input(
            "Decision Title",
            placeholder=(
                "Example: Choose database for project"
            )
        )

        description = st.text_area(
            "Decision Description",
            placeholder=(
                "Explain the problem and "
                "why a decision is required."
            ),
            height=150
        )

        options = st.text_area(
            "Available Options",
            placeholder=(
                "Option A: MySQL\n"
                "Option B: PostgreSQL\n"
                "Option C: MongoDB"
            ),
            height=120
        )

        # ----------------------------------------------------
        # AI BUTTON
        # ----------------------------------------------------

        if st.button(
            "🤖 Get Gemini AI Suggestion",
            use_container_width=True
        ):

            if (
                not title.strip()
                or not description.strip()
                or not options.strip()
            ):

                st.warning(
                    "Please fill in all fields."
                )

            else:

                with st.spinner(
                    "Gemini is analyzing your decision..."
                ):

                    (
                        suggestion,
                        risk,
                        recommendation
                    ) = get_ai_suggestion(
                        title,
                        description,
                        options
                    )

                st.session_state.ai_result = {

                    "title": title,

                    "description": description,

                    "options": options,

                    "suggestion": suggestion,

                    "risk": risk,

                    "recommendation": recommendation
                }

        # ----------------------------------------------------
        # SHOW AI RESULT
        # ----------------------------------------------------

        if "ai_result" in st.session_state:

            ai = st.session_state.ai_result

            st.divider()

            st.subheader(
                "🤖 Gemini AI Decision Support"
            )

            st.markdown(
                "### 💡 AI Suggestion"
            )

            st.info(
                ai["suggestion"]
            )

            st.markdown(
                "### ⚠️ Risk Analysis"
            )

            st.warning(
                ai["risk"]
            )

            st.markdown(
                "### 🎯 AI Recommendation"
            )

            st.success(
                ai["recommendation"]
            )

            st.caption(
                "AI provides decision support only. "
                "The manager makes the final decision."
            )

            # ------------------------------------------------
            # SUBMIT
            # ------------------------------------------------

            if st.button(
                "📤 Submit Decision to Manager",
                use_container_width=True
            ):

                decisions = load_decisions()

                new_id = (
                    max(
                        [
                            d.get("id", 0)
                            for d in decisions
                        ],
                        default=0
                    )
                    + 1
                )

                decision = Decision(

                    id=new_id,

                    employee=(
                        st.session_state.username
                    ),

                    title=ai["title"],

                    description=ai["description"],

                    options=ai["options"],

                    ai_suggestion=(
                        ai["suggestion"]
                    ),

                    ai_risk=(
                        ai["risk"]
                    ),

                    ai_recommendation=(
                        ai["recommendation"]
                    ),

                    status="Pending",

                    manager_comment="",

                    created_at=(
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    ),

                    reviewed_at=""
                )

                decisions.append(
                    decision.model_dump()
                )

                save_decisions(
                    decisions
                )

                st.session_state.pop(
                    "ai_result",
                    None
                )

                st.success(
                    "✅ Decision submitted to manager!"
                )

                st.rerun()

    # ========================================================
    # MY DECISIONS
    # ========================================================

    with decisions_tab:

        st.subheader(
            "📋 My Decisions"
        )

        decisions = load_decisions()

        my_decisions = [

            d for d in decisions

            if d.get("employee")
            == st.session_state.username
        ]

        if not my_decisions:

            st.info(
                "You have not created any decisions yet."
            )

        for decision in reversed(
            my_decisions
        ):

            status = decision.get(
                "status",
                "Pending"
            )

            with st.expander(
                f"#{decision['id']} | "
                f"{decision['title']} | "
                f"{status}"
            ):

                st.write(
                    f"**Description:** "
                    f"{decision['description']}"
                )

                st.write(
                    f"**Options:** "
                    f"{decision['options']}"
                )

                st.markdown(
                    "### 💡 AI Suggestion"
                )

                st.info(
                    decision.get(
                        "ai_suggestion",
                        ""
                    )
                )

                st.markdown(
                    "### ⚠️ Risk Analysis"
                )

                st.warning(
                    decision.get(
                        "ai_risk",
                        ""
                    )
                )

                st.markdown(
                    "### 🎯 AI Recommendation"
                )

                st.success(
                    decision.get(
                        "ai_recommendation",
                        ""
                    )
                )

                st.divider()

                if status == "Pending":

                    st.warning(
                        "⏳ Waiting for manager approval."
                    )

                elif status == "Approved":

                    st.success(
                        "✅ Decision Approved"
                    )

                elif status == "Rejected":

                    st.error(
                        "❌ Decision Rejected"
                    )

                if decision.get(
                    "manager_comment"
                ):

                    st.write(
                        f"**Manager Comment:** "
                        f"{decision['manager_comment']}"
                    )

                if decision.get(
                    "reviewed_at"
                ):

                    st.write(
                        f"**Reviewed At:** "
                        f"{decision['reviewed_at']}"
                    )


# ============================================================
# MANAGER DASHBOARD
# ============================================================

def manager_dashboard():

    st.title(
        "👨‍💼 Manager Dashboard"
    )

    st.write(
        "Review employee decisions and make "
        "the final approval or rejection."
    )

    decisions = load_decisions()

    pending = [
        d for d in decisions
        if d.get("status") == "Pending"
    ]

    approved = [
        d for d in decisions
        if d.get("status") == "Approved"
    ]

    rejected = [
        d for d in decisions
        if d.get("status") == "Rejected"
    ]

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "⏳ Pending",
        len(pending)
    )

    col2.metric(
        "✅ Approved",
        len(approved)
    )

    col3.metric(
        "❌ Rejected",
        len(rejected)
    )

    st.divider()

    if not decisions:

        st.info(
            "No employee decisions available."
        )

        return

    # ========================================================
    # DECISION LIST
    # ========================================================

    for decision in reversed(
        decisions
    ):

        st.subheader(
            f"#{decision['id']} - "
            f"{decision['title']}"
        )

        st.write(
            f"👤 Employee: "
            f"**{decision['employee']}**"
        )

        st.write(
            f"📅 Created: "
            f"{decision['created_at']}"
        )

        st.write(
            f"📌 Status: "
            f"**{decision['status']}**"
        )

        st.write(
            f"**Description:** "
            f"{decision['description']}"
        )

        st.write(
            f"**Options:** "
            f"{decision['options']}"
        )

        # ----------------------------------------------------
        # AI INFORMATION
        # ----------------------------------------------------

        st.markdown(
            "### 💡 Gemini AI Suggestion"
        )

        st.info(
            decision.get(
                "ai_suggestion",
                ""
            )
        )

        st.markdown(
            "### ⚠️ Risk Analysis"
        )

        st.warning(
            decision.get(
                "ai_risk",
                ""
            )
        )

        st.markdown(
            "### 🎯 AI Recommendation"
        )

        st.success(
            decision.get(
                "ai_recommendation",
                ""
            )
        )

        # ====================================================
        # MANAGER REVIEW
        # ====================================================

        if decision["status"] == "Pending":

            manager_comment = st.text_area(
                "Manager Comment",
                key=f"comment_{decision['id']}",
                placeholder=(
                    "Enter your reason for "
                    "approval or rejection..."
                )
            )

            col1, col2 = st.columns(2)

            # ------------------------------------------------
            # APPROVE
            # ------------------------------------------------

            with col1:

                if st.button(
                    "✅ Approve Decision",
                    key=f"approve_{decision['id']}",
                    use_container_width=True
                ):

                    for d in decisions:

                        if d["id"] == decision["id"]:

                            d["status"] = "Approved"

                            d["manager_comment"] = (
                                manager_comment
                            )

                            d["reviewed_at"] = (
                                datetime.now().strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                )
                            )

                    save_decisions(
                        decisions
                    )

                    st.success(
                        "✅ Decision approved!"
                    )

                    st.rerun()

            # ------------------------------------------------
            # REJECT
            # ------------------------------------------------

            with col2:

                if st.button(
                    "❌ Reject Decision",
                    key=f"reject_{decision['id']}",
                    use_container_width=True
                ):

                    if not manager_comment.strip():

                        st.warning(
                            "Please enter a reason "
                            "before rejecting."
                        )

                    else:

                        for d in decisions:

                            if d["id"] == decision["id"]:

                                d["status"] = "Rejected"

                                d["manager_comment"] = (
                                    manager_comment
                                )

                                d["reviewed_at"] = (
                                    datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    )
                                )

                        save_decisions(
                            decisions
                        )

                        st.error(
                            "❌ Decision rejected."
                        )

                        st.rerun()

        # ====================================================
        # ALREADY REVIEWED
        # ====================================================

        else:

            if decision.get(
                "manager_comment"
            ):

                st.write(
                    f"**Manager Comment:** "
                    f"{decision['manager_comment']}"
                )

            if decision.get(
                "reviewed_at"
            ):

                st.write(
                    f"**Reviewed At:** "
                    f"{decision['reviewed_at']}"
                )

        st.divider()


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Session state
    # --------------------------------------------------------

    if "logged_in" not in st.session_state:

        st.session_state.logged_in = False

    # --------------------------------------------------------
    # Login
    # --------------------------------------------------------

    if not st.session_state.logged_in:

        login_page()

        return

    # --------------------------------------------------------
    # Sidebar
    # --------------------------------------------------------

    sidebar()

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    if st.session_state.role == "Employee":

        employee_dashboard()

    elif st.session_state.role == "Manager":

        manager_dashboard()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()