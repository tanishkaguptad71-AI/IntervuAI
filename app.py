import streamlit as st
import time
import io
import re
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)

# ==================================================
# INTERVUAI - AI MOCK INTERVIEW SYSTEM
# 5 QUESTIONS | 10 MARKS EACH | 5 MINUTES
# ==================================================

st.set_page_config(
    page_title="IntervuAI",
    page_icon="🎯",
    layout="wide"
)

# ---------------- DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #10132b, #202044);
    color: #f5f3ff;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, h4, p, label {
    color: #f5f3ff !important;
}
.hero-title {
    font-size: 2.7rem;
    font-weight: 850;
    color: #c5b5ff;
}
.hero-subtitle {
    color: #d2cdef;
    font-size: 1rem;
}
.panel {
    background: #2b2a4f;
    border: 1px solid rgba(185,165,255,.22);
    padding: 22px;
    border-radius: 16px;
    margin: 10px 0 18px 0;
}
div.stButton > button,
div.stDownloadButton > button {
    background: #8064e9;
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: 700;
    min-height: 2.7rem;
}
div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background: #9a83ff;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="hero-title">IntervuAI 🎯</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">Your Personal AI-Powered Mock Interview Platform</div>',
    unsafe_allow_html=True
)


# ---------------- QUESTION BANK ----------------
# Every question has its own expected concepts.

QUESTION_BANK = {
    "AI/ML Engineer": {
        "Beginner": [
            ("What is Artificial Intelligence, and where is it used?",
             ["machines", "intelligence", "tasks", "data", "automation"]),
            ("What is Machine Learning?",
             ["data", "learn", "patterns", "model", "prediction"]),
            ("What is the difference between AI and ML?",
             ["artificial intelligence", "machine learning", "subset", "systems", "data"]),
            ("What is a dataset in machine learning?",
             ["collection", "data", "examples", "training", "testing"]),
            ("What is a feature in a machine learning dataset?",
             ["input", "variable", "attribute", "data", "prediction"])
        ],

        "Intermediate": [
            ("Explain the steps in a supervised machine learning workflow.",
             ["data", "preprocessing", "training", "model", "evaluation", "testing"]),
            ("What is the difference between classification and regression?",
             ["classification", "categories", "regression", "continuous", "values"]),
            ("What is overfitting, and how can it be reduced?",
             ["training", "unseen", "generalization", "regularization", "validation"]),
            ("Why do we split data into training and testing sets?",
             ["training", "testing", "unseen", "performance", "generalization"]),
            ("What is a confusion matrix used for?",
             ["actual", "predicted", "true positive", "false positive", "classification"])
        ],

        "Advanced": [
            ("How would you handle an imbalanced classification dataset?",
             ["class weights", "resampling", "oversampling", "undersampling", "precision", "recall"]),
            ("Explain the bias-variance trade-off.",
             ["bias", "variance", "underfitting", "overfitting", "generalization"]),
            ("How would you select an evaluation metric for classification?",
             ["precision", "recall", "f1", "accuracy", "false positive", "false negative"]),
            ("What is data leakage, and why is it dangerous?",
             ["training", "testing", "information", "leak", "future", "evaluation"]),
            ("How would you monitor a machine learning model after deployment?",
             ["performance", "drift", "monitoring", "data", "retraining", "feedback"])
        ]
    },

    "Python Developer": {
        "Beginner": [
            ("What is Python, and mention two uses of it?",
             ["programming", "language", "automation", "web", "data"]),
            ("What is the difference between a list and a tuple?",
             ["mutable", "immutable", "list", "tuple", "elements"]),
            ("What is a variable in Python?",
             ["name", "store", "value", "data", "memory"]),
            ("What is a function in Python?",
             ["reusable", "code", "def", "parameters", "return"]),
            ("What is a dictionary in Python?",
             ["key", "value", "pairs", "mapping", "mutable"])
        ],

        "Intermediate": [
            ("Explain exception handling using try and except.",
             ["try", "except", "error", "exception", "finally"]),
            ("What is the difference between list comprehension and a normal loop?",
             ["list", "comprehension", "loop", "expression", "iterable"]),
            ("Explain the purpose of modules and packages.",
             ["module", "package", "organize", "reuse", "import"]),
            ("What is object-oriented programming in Python?",
             ["class", "object", "inheritance", "encapsulation", "methods"]),
            ("What is the difference between == and is in Python?",
             ["equality", "identity", "value", "object", "memory"])
        ],

        "Advanced": [
            ("Explain decorators and give a typical use case.",
             ["function", "wrapper", "decorator", "metadata", "behavior"]),
            ("What are generators, and how do they help memory usage?",
             ["yield", "iterator", "lazy", "memory", "values"]),
            ("Explain Python's Global Interpreter Lock.",
             ["gil", "thread", "lock", "bytecode", "parallel"]),
            ("How would you structure a maintainable Python application?",
             ["modules", "separation", "testing", "configuration", "readability"]),
            ("What is the difference between concurrency and parallelism?",
             ["concurrency", "parallelism", "tasks", "simultaneously", "execution"])
        ]
    },

    "Software Engineer": {
        "Beginner": [
            ("What is the Software Development Life Cycle?",
             ["planning", "design", "development", "testing", "maintenance"]),
            ("What is an algorithm?",
             ["steps", "problem", "solution", "finite", "instructions"]),
            ("What is debugging?",
             ["errors", "bugs", "identify", "fix", "program"]),
            ("What is the difference between a compiler and an interpreter?",
             ["compiler", "interpreter", "translate", "execute", "code"]),
            ("What is object-oriented programming?",
             ["objects", "classes", "data", "methods", "reuse"])
        ],

        "Intermediate": [
            ("Explain the four main principles of object-oriented programming.",
             ["encapsulation", "inheritance", "polymorphism", "abstraction"]),
            ("What is the difference between a process and a thread?",
             ["process", "thread", "memory", "resources", "execution"]),
            ("Why are data structures important in software development?",
             ["organize", "data", "operations", "efficiency", "access"]),
            ("What is version control, and why do teams use Git?",
             ["history", "changes", "collaboration", "branch", "merge"]),
            ("Explain unit testing and integration testing.",
             ["unit", "component", "integration", "modules", "testing"])
        ],

        "Advanced": [
            ("How would you design a system to handle increasing user traffic?",
             ["scaling", "load balancing", "caching", "database", "monitoring"]),
            ("Explain the SOLID principles and their purpose.",
             ["single responsibility", "open closed", "liskov", "interface segregation", "dependency"]),
            ("What is the difference between monolithic and microservices architecture?",
             ["monolithic", "microservices", "services", "deployment", "communication"]),
            ("How would you investigate a slow production application?",
             ["profiling", "logs", "metrics", "database", "bottleneck"]),
            ("Explain database transactions and ACID properties.",
             ["atomicity", "consistency", "isolation", "durability", "transaction"])
        ]
    },

    "Web Developer": {
        "Beginner": [
            ("What is HTML used for?",
             ["structure", "webpage", "elements", "content", "browser"]),
            ("What is CSS used for?",
             ["style", "layout", "color", "design", "webpage"]),
            ("What is JavaScript used for in a website?",
             ["interaction", "behavior", "dynamic", "browser", "function"]),
            ("What is the role of a web browser?",
             ["request", "render", "html", "css", "javascript"]),
            ("What is the difference between frontend and backend?",
             ["frontend", "interface", "backend", "server", "database"])
        ],

        "Intermediate": [
            ("What is responsive web design?",
             ["screen", "device", "flexible", "media queries", "layout"]),
            ("Explain how HTTP requests and responses work.",
             ["client", "request", "server", "response", "http"]),
            ("What is the Document Object Model?",
             ["dom", "document", "tree", "elements", "javascript"]),
            ("What is an API, and how does a frontend use one?",
             ["interface", "request", "response", "data", "endpoint"]),
            ("Why is form validation important?",
             ["input", "validation", "errors", "security", "user"])
        ],

        "Advanced": [
            ("How would you improve the performance of a slow website?",
             ["optimization", "caching", "images", "javascript", "loading"]),
            ("Explain cross-site scripting and how to reduce its risk.",
             ["xss", "script", "input", "sanitize", "escape"]),
            ("What is the purpose of authentication and authorization?",
             ["identity", "authentication", "permission", "authorization", "access"]),
            ("How would you make a web application accessible?",
             ["keyboard", "screen reader", "semantic", "contrast", "aria"]),
            ("Explain server-side rendering and client-side rendering.",
             ["server", "client", "render", "html", "performance"])
        ]
    }
}


# ---------------- ANSWER EVALUATION ----------------

def evaluate_answer(answer, keywords):

    text = answer.lower().strip()
    words = re.findall(r"[a-zA-Z0-9+#.-]+", text)

    if not words:
        return 0, "No answer submitted.", []

    matched = []

    for keyword in keywords:
        if keyword.lower() in text:
            matched.append(keyword)

    coverage = len(matched) / len(keywords)

    # Concept coverage contributes up to 8 marks.
    concept_score = coverage * 8

    # Length contributes only a small amount.
    word_count = len(words)

    if word_count < 5:
        clarity_score = 0
    elif word_count < 12:
        clarity_score = 0.5
    elif word_count < 25:
        clarity_score = 1
    else:
        clarity_score = 2

    score = min(10, round(concept_score + clarity_score))

    if score >= 8:
        feedback = (
            "Strong coverage of the expected concepts. "
            "Keep your explanation clear and accurate."
        )
    elif score >= 5:
        feedback = (
            "Partially covered. Add more important concepts "
            "and explain how they relate."
        )
    elif score >= 3:
        feedback = (
            "Some relevant ideas are present, but the answer "
            "needs more key concepts and explanation."
        )
    else:
        feedback = (
            "The answer has limited coverage of the expected concepts. "
            "Review the topic and try again."
        )

    if word_count < 5:
        feedback += " Your answer is too short to demonstrate understanding."

    return score, feedback, matched


# ---------------- PDF REPORT ----------------

def make_pdf(candidate, results, total_score, profile):

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=42,
        leftMargin=42,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#5941A9"),
        alignment=TA_CENTER,
        fontSize=19
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        spaceAfter=5
    )

    story = [
        Paragraph(
            "IntervuAI - Interview Performance Report",
            title_style
        ),
        Spacer(1, 16),

        Paragraph(
            f"<b>Candidate:</b> {escape(candidate['name'])}",
            body_style
        ),
        Paragraph(
            f"<b>Email:</b> {escape(candidate['email'])}",
            body_style
        ),
        Paragraph(
            f"<b>College:</b> {escape(candidate['college'])}",
            body_style
        ),
        Paragraph(
            f"<b>Course / Branch:</b> {escape(candidate['course'])}",
            body_style
        ),
        Paragraph(
            f"<b>Job Role:</b> {escape(profile['role'])}",
            body_style
        ),
        Paragraph(
            f"<b>Experience:</b> {escape(profile['experience'])}",
            body_style
        ),
        Paragraph(
            f"<b>Difficulty:</b> {escape(profile['difficulty'])}",
            body_style
        ),
        Paragraph(
            f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y %I:%M %p')}",
            body_style
        ),
        Spacer(1, 14)
    ]

    table_data = [
        ["Question", "Marks", "Concepts Identified"]
    ]

    for i, item in enumerate(results, start=1):

        concepts = ", ".join(item["matched"])

        if not concepts:
            concepts = "Limited"

        table_data.append([
            Paragraph(
                f"Q{i}. {escape(item['question'])}",
                body_style
            ),
            f"{item['score']}/10",
            Paragraph(escape(concepts), body_style)
        ])

    table = Table(
        table_data,
        colWidths=[245, 55, 165],
        repeatRows=1
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5941A9")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    story.append(table)
    story.append(Spacer(1, 14))

    percentage = total_score / 50 * 100

    story.append(
        Paragraph(
            f"<b>Total Score: {total_score}/50 ({percentage:.1f}%)</b>",
            styles["Heading2"]
        )
    )

    if percentage >= 80:
        overall = "Strong performance"
    elif percentage >= 60:
        overall = "Good foundation; some areas need improvement"
    elif percentage >= 40:
        overall = "Developing; revise key concepts and practise"
    else:
        overall = "Needs more preparation and practice"

    story.append(
        Paragraph(
            f"<b>Overall Feedback:</b> {overall}",
            body_style
        )
    )

    story.append(Spacer(1, 12))
    story.append(
        Paragraph("Detailed Answer Feedback", styles["Heading2"])
    )

    for i, item in enumerate(results, start=1):

        story.append(Spacer(1, 7))

        story.append(
            Paragraph(
                f"<b>Question {i}:</b> {escape(item['question'])}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Answer:</b> {escape(item['answer'])}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Score:</b> {item['score']}/10",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Feedback:</b> {escape(item['feedback'])}",
                body_style
            )
        )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<i>Scoring note: Scores are estimated using expected "
            "keyword coverage and answer clarity. They are intended "
            "for practice, not as a validated measure of technical ability.</i>",
            body_style
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer


# ---------------- SESSION STATE ----------------

STATE_DEFAULTS = {
    "started": False,
    "finished": False,
    "candidate": {},
    "profile": {},
    "questions": [],
    "question_index": 0,
    "results": [],
    "start_time": None,
    "time_up": False
}

for key, value in STATE_DEFAULTS.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- CANDIDATE REGISTRATION ----------------

if not st.session_state.started and not st.session_state.finished:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.header("Candidate Registration")

    st.write(
        "Enter your details to personalise your mock interview."
    )

    with st.form("candidate_form"):

        col1, col2 = st.columns(2)

        with col1:

            full_name = st.text_input("Full Name *")

            email = st.text_input("Email Address *")

            college = st.text_input("College / University *")

        with col2:

            course = st.text_input("Course / Branch *")

            role = st.selectbox(
                "Target Job Role",
                list(QUESTION_BANK.keys())
            )

            experience = st.selectbox(
                "Experience Level",
                [
                    "Student / Fresher",
                    "Less than 1 year",
                    "1–3 years",
                    "3+ years"
                ]
            )

        difficulty = st.selectbox(
            "Interview Difficulty",
            ["Beginner", "Intermediate", "Advanced"]
        )

        st.caption(
            "Interview Format: 5 Questions | 10 Marks Each | 5 Minutes"
        )

        submitted = st.form_submit_button(
            "Start Interview",
            use_container_width=True
        )

    if submitted:

        if not all([
            full_name.strip(),
            email.strip(),
            college.strip(),
            course.strip()
        ]):

            st.error("Please complete all required fields.")

        elif not re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email.strip()
        ):

            st.error("Please enter a valid email address.")

        else:

            st.session_state.candidate = {
                "name": full_name.strip(),
                "email": email.strip(),
                "college": college.strip(),
                "course": course.strip()
            }

            st.session_state.profile = {
                "role": role,
                "experience": experience,
                "difficulty": difficulty
            }

            st.session_state.questions = QUESTION_BANK[role][difficulty]

            st.session_state.question_index = 0

            st.session_state.results = []

            st.session_state.start_time = time.time()

            st.session_state.time_up = False

            st.session_state.started = True

            st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ---------------- TIMER ----------------

@st.fragment(run_every=1)
def render_timer():

    if st.session_state.started and not st.session_state.finished:

        elapsed = int(
            time.time() - st.session_state.start_time
        )

        remaining = max(0, 300 - elapsed)

        minutes, seconds = divmod(remaining, 60)

        st.metric(
            "Time Remaining",
            f"{minutes:02d}:{seconds:02d}"
        )

        if remaining == 0 and not st.session_state.time_up:

            st.session_state.time_up = True

            st.warning(
                "Time is up. Submit your current answer or finish the interview."
            )


# ---------------- INTERVIEW SCREEN ----------------

if st.session_state.started and not st.session_state.finished:

    candidate = st.session_state.candidate

    profile = st.session_state.profile

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.subheader(
        f"Welcome, {candidate['name']}!"
    )

    st.write(
        f"**Role:** {profile['role']}  |  "
        f"**Difficulty:** {profile['difficulty']}  |  "
        f"**Experience:** {profile['experience']}"
    )

    st.caption(
        "Your answers are evaluated for relevant concepts and explanation quality."
    )

    render_timer()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )
    q_index = st.session_state.question_index

    questions = st.session_state.questions

    question, keywords = questions[q_index]

    st.progress(
        (q_index + 1) / 5,
        text=f"Question {q_index + 1} of 5"
    )

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.subheader(
        f"Question {q_index + 1}"
    )

    st.markdown(
        f"### {question}"
    )

    st.caption("Maximum Marks: 10")

    answer = st.text_area(
        "Your Answer",
        key=f"answer_{q_index}",
        height=170,
        placeholder=(
            "Explain the concept in your own words. "
            "Include important points and an example where relevant."
        )
    )
    left, right = st.columns(2)

    with left:

        submit_answer = st.button(
            "Submit Answer",
            use_container_width=True
        )

    with right:

        finish_early = st.button(
            "Finish Interview",
            use_container_width=True
        )

    if submit_answer:

        if not answer.strip():

            st.error("Please enter an answer before submitting.")

        else:

            score, feedback, matched = evaluate_answer(
                answer,
                keywords
            )

            st.session_state.results.append({
                "question": question,
                "answer": answer.strip(),
                "score": score,
                "feedback": feedback,
                "matched": matched
            })

            if q_index < 4:

                st.session_state.question_index += 1

                st.rerun()

            else:

                st.session_state.finished = True

                st.rerun()

    if finish_early:

        already_answered = len(
            st.session_state.results
        )

        for j in range(already_answered, 5):

            q, _ = questions[j]

            st.session_state.results.append({
                "question": q,
                "answer": "Not answered",
                "score": 0,
                "feedback": "This question was not answered.",
                "matched": []
            })

        st.session_state.finished = True

        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ---------------- RESULTS DASHBOARD ----------------
if st.session_state.finished:

    candidate = st.session_state.candidate

    profile = st.session_state.profile

    results = st.session_state.results

    total_score = sum(
        item["score"] for item in results
    )

    percentage = total_score / 50 * 100

    st.title("Interview Results")

    st.success(
        f"Interview completed, {candidate['name']}!"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Score",
        f"{total_score}/50"
    )

    col2.metric(
        "Percentage",
        f"{percentage:.1f}%"
    )

    answered_count = sum(
        1 for item in results
        if item["answer"] != "Not answered"
    )

    col3.metric(
        "Questions Answered",
        f"{answered_count}/5"
    )

    if percentage >= 80:

        overall = "Strong Performance"

        advice = (
            "You demonstrated good coverage of the expected concepts. "
            "Keep practising with real examples."
        )

    elif percentage >= 60:

        overall = "Good Foundation"

        advice = (
            "You understand several key ideas. "
            "Work on missing concepts and clearer explanations."
        )

    elif percentage >= 40:

        overall = "Developing"

        advice = (
            "Revise the fundamentals and practise explaining "
            "each topic step by step."
        )

    else:

        overall = "Needs More Preparation"

        advice = (
            "Start with the basic concepts, then practise "
            "short explanations and examples."
        )

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.subheader(overall)

    st.write(advice)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader("Question-wise Scores")

    st.bar_chart({
        f"Question {i + 1}": item["score"]
        for i, item in enumerate(results)
    })

    st.subheader("Detailed Feedback")

    for i, item in enumerate(results):

        with st.expander(
            f"Question {i + 1} — {item['score']}/10"
        ):

            st.write(
                "**Question:**",
                item["question"]
            )

            st.write(
                "**Your Answer:**",
                item["answer"]
            )

            st.write(
                "**Score:**",
                f"{item['score']}/10"
            )

            st.write(
                "**Feedback:**",
                item["feedback"]
            )

            if item["matched"]:

                st.write(
                    "**Expected Concepts Identified:**",
                    ", ".join(item["matched"])
                )

            else:

                st.write(
                    "**Expected Concepts Identified:** None"
                )

    st.caption(
        "Scoring is an indicative keyword-based practice estimate. "
        "It does not independently verify every technical claim."
    )

    # PDF DOWNLOAD

    pdf = make_pdf(
        candidate,
        results,
        total_score,
        profile
    )

    st.download_button(
        "Download Detailed PDF Report",
        data=pdf,
        file_name=(
            f"IntervuAI_Report_"
            f"{candidate['name'].replace(' ', '_')}.pdf"
        ),
        mime="application/pdf",
        use_container_width=True
    )

    # NEW INTERVIEW

    if st.button(
        "Start New Interview",
        use_container_width=True
    ):

        for key in STATE_DEFAULTS:

            if key in st.session_state:

                del st.session_state[key]

        st.rerun()