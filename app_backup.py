import streamlit as st
import time
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

from ml_model import model, vectorizer


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="IntervuAI",
    page_icon="🎯",
    layout="centered"
)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0b1020, #17152e);
        color: #ffffff;
    }

    h1 {
        color: #a78bfa !important;
        font-size: 42px !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: #e9d5ff !important;
    }

    p, label, span {
        color: #e2e8f0;
    }

    div[data-testid="stMetric"] {
        background: #24213f;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #514477;
    }

    .stButton > button {
        background: linear-gradient(90deg, #7c3aed, #a855f7);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 22px;
        font-weight: bold;
        width: 100%;
    }

    .stButton > button:hover {
        background: #6d28d9;
        color: white;
        border: 1px solid #c4b5fd;
    }

    .stTextInput input, .stTextArea textarea {
        background: #24213f;
        color: white;
        border-radius: 10px;
    }

    div[data-testid="stProgressBar"] > div {
        background-color: #a78bfa;
    }

    hr {
        border-color: #514477;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background: linear-gradient(120deg, #312e81, #7c3aed);
    padding: 28px;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 25px;
">
    <h1 style="color:white !important; margin:0;">
        🎯 IntervuAI
    </h1>
    <p style="color:#ede9fe !important; font-size:18px;">
        Your Personal AI Interview Preparation Platform
    </p>
    <p style="color:#ddd6fe !important;">
        Practice • Improve • Succeed
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. INTERVIEW QUESTIONS
# ==========================================

role_questions = {

    "Python Developer": {
        "Beginner": [
            "Tell me about yourself.",
            "What is Python?",
            "What are functions in Python?"
        ],
        "Intermediate": [
            "Explain the difference between a list and a tuple.",
            "What is exception handling in Python?",
            "Explain object-oriented programming in Python."
        ],
        "Advanced": [
            "How does memory management work in Python?",
            "Explain decorators and their use cases.",
            "How would you improve Python application performance?"
        ]
    },

    "AI/ML Engineer": {
        "Beginner": [
            "Tell me about yourself.",
            "What is Machine Learning?",
            "What is the difference between AI and ML?"
        ],
        "Intermediate": [
            "Explain supervised and unsupervised learning.",
            "What is overfitting in Machine Learning?",
            "What is the purpose of training and testing data?"
        ],
        "Advanced": [
            "How would you handle an imbalanced dataset?",
            "Explain the bias-variance trade-off.",
            "How would you deploy and monitor an ML model?"
        ]
    },

    "Web Developer": {
        "Beginner": [
            "Tell me about yourself.",
            "What is HTML?",
            "What is the difference between HTML and CSS?"
        ],
        "Intermediate": [
            "Explain the DOM in JavaScript.",
            "What is responsive web design?",
            "What is the difference between GET and POST?"
        ],
        "Advanced": [
            "How would you improve website performance?",
            "Explain cross-site scripting and how to prevent it.",
            "How would you design a scalable web application?"
        ]
    }
}


# ==========================================
# 3. EXPECTED KEYWORDS
# ==========================================

role_keywords = {

    "Python Developer": {
        "Beginner": [
            ["student", "skills", "experience", "project"],
            ["programming", "language", "code", "automation"],
            ["function", "reusable", "code", "parameter", "return"]
        ],
        "Intermediate": [
            ["list", "tuple", "mutable", "immutable"],
            ["exception", "error", "try", "except"],
            ["object", "class", "inheritance", "encapsulation"]
        ],
        "Advanced": [
            ["memory", "garbage", "reference", "allocation"],
            ["decorator", "function", "wrapper"],
            ["performance", "optimization", "profiling", "efficient"]
        ]
    },

    "AI/ML Engineer": {
        "Beginner": [
            ["student", "skills", "experience", "project"],
            ["data", "algorithm", "learn", "prediction", "model"],
            ["artificial intelligence", "machine learning", "intelligence"]
        ],
        "Intermediate": [
            ["supervised", "unsupervised", "label", "data"],
            ["overfitting", "training", "model", "generalization"],
            ["training", "testing", "dataset", "accuracy"]
        ],
        "Advanced": [
            ["imbalanced", "sampling", "class", "dataset"],
            ["bias", "variance", "trade"],
            ["deploy", "monitor", "model", "performance"]
        ]
    },

    "Web Developer": {
        "Beginner": [
            ["student", "skills", "experience", "project"],
            ["markup", "web", "structure", "tags", "html"],
            ["html", "css", "structure", "style"]
        ],
        "Intermediate": [
            ["dom", "document", "elements", "javascript"],
            ["responsive", "mobile", "screen", "layout"],
            ["get", "post", "request", "server"]
        ],
        "Advanced": [
            ["performance", "loading", "optimization", "cache"],
            ["cross-site scripting", "xss", "script", "input"],
            ["scalable", "architecture", "server", "database"]
        ]
    }
}


# ==========================================
# 4. SESSION STATE
# ==========================================

defaults = {
    "interview_started": False,
    "submitted": False,
    "current_question": 0,
    "candidate_name": "",
    "candidate_role": "Python Developer",
    "candidate_difficulty": "Beginner",
    "start_time": 0.0,
    "results": [],
    "overall_score": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# 5. PDF REPORT GENERATOR
# ==========================================

def generate_pdf_report(
    name, role, difficulty,
    questions, answers, results, overall_score
):

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    def write_line(text, bold=False):

        nonlocal y

        font = "Helvetica-Bold" if bold else "Helvetica"
        pdf.setFont(font, 10)

        safe_text = str(text).encode(
            "latin-1", "replace"
        ).decode("latin-1")

        lines = simpleSplit(
            safe_text, font, 10, width - 100
        )

        for line in lines:

            if y < 50:
                pdf.showPage()
                y = height - 50

            pdf.drawString(50, y, line)
            y -= 16

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "IntervuAI Interview Report")
    y -= 35

    write_line(f"Candidate: {name}")
    write_line(f"Job Role: {role}")
    write_line(f"Difficulty: {difficulty}")
    write_line(f"Overall Score: {overall_score:.0f}/100", True)

    y -= 15

    for i in range(len(questions)):

        write_line(f"Question {i + 1}: {questions[i]}", True)
        write_line(f"Answer: {answers[i]}")
        write_line(f"Evaluation: {results[i]['prediction']}")
        write_line(f"Score: {results[i]['score']}/100")

        y -= 12

    write_line(
        "Note: This is an educational ML prototype. Scores are illustrative."
    )

    pdf.save()
    buffer.seek(0)

    return buffer.getvalue()


# ==========================================
# 6. CANDIDATE DETAILS
# ==========================================

st.subheader("Candidate Details")

name = st.text_input(
    "Enter your name",
    key="candidate_name_input"
)

role = st.selectbox(
    "Select your job role",
    [
        "Python Developer",
        "AI/ML Engineer",
        "Web Developer"
    ]
)

difficulty = st.selectbox(
    "Select interview difficulty",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


# ==========================================
# 7. START INTERVIEW
# ==========================================

if st.button("Start Interview"):

    if not name.strip():

        st.warning("Please enter your name.")

    else:

        st.session_state.interview_started = True
        st.session_state.submitted = False
        st.session_state.current_question = 0

        st.session_state.candidate_name = name
        st.session_state.candidate_role = role
        st.session_state.candidate_difficulty = difficulty

        st.session_state.start_time = time.time()

        st.session_state.results = []
        st.session_state.overall_score = 0

        for i in range(3):
            st.session_state[f"answer_{i}"] = ""

        st.rerun()


# ==========================================
# 8. LIVE TIMER AND INTERVIEW
# ==========================================

@st.fragment(run_every=1)
def interview_panel():

    if not st.session_state.interview_started:
        return

    if st.session_state.submitted:
        return

    selected_role = st.session_state.candidate_role
    selected_difficulty = st.session_state.candidate_difficulty

    questions = role_questions[selected_role][selected_difficulty]

    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 300 - int(elapsed))

    minutes = remaining // 60
    seconds = remaining % 60

    st.divider()

    st.success(
        f"Welcome {st.session_state.candidate_name}!"
    )

    st.write("Job Role:", selected_role)
    st.write("Difficulty:", selected_difficulty)

    st.metric(
        "Time Remaining",
        f"{minutes:02d}:{seconds:02d}"
    )

    # TIME EXPIRED

    if remaining == 0:

        st.error("Your interview time has ended.")

        if st.button("Restart Interview"):

            st.session_state.interview_started = False
            st.session_state.submitted = False
            st.session_state.current_question = 0

            st.rerun()

        return

    # CURRENT QUESTION

    current = st.session_state.current_question

    st.progress((current + 1) / 3)

    st.write(f"Question {current + 1} of 3")
    st.subheader(questions[current])

    st.text_area(
    "Write your answer below:",
    key=f"answer_{current}",
    placeholder="Type your answer here..."
)

    # NEXT QUESTION

    if current < 2:

        if st.button("Next Question"):

            answer = st.session_state.get(
                f"answer_{current}", ""
            )

            if not answer.strip():

                st.warning("Please answer this question first.")

            elif time.time() - st.session_state.start_time >= 300:

                st.error("Your interview time has ended.")

            else:

                st.session_state.current_question += 1
                st.rerun()

    # SUBMIT INTERVIEW

    else:

        if st.button("Submit Interview"):

            answer = st.session_state.get("answer_2", "")

            if not answer.strip():

                st.warning("Please answer this question first.")

            elif time.time() - st.session_state.start_time >= 300:

                st.error("Your interview time has ended.")

            else:

                st.session_state.submitted = True
                st.rerun()


if (
    st.session_state.interview_started
    and not st.session_state.submitted
):
    interview_panel()


# ==========================================
# 9. AI EVALUATION
# ==========================================

if (
    st.session_state.interview_started
    and st.session_state.submitted
):

    st.divider()
    st.subheader("AI Evaluation")

    selected_role = st.session_state.candidate_role
    selected_difficulty = st.session_state.candidate_difficulty
    questions = role_questions[selected_role][selected_difficulty]
    keywords_list = role_keywords[selected_role][selected_difficulty]


    score_map = {
        "Good": 100,
        "Average": 60,
        "Needs Improvement": 30
    }

    results = []
    total_score = 0

    answers = []

answers = []

for i in range(3):
    saved_answer = st.session_state.get(f"answer_{i}", "")
    answers.append(saved_answer.strip())

    for i in range(3):

        answer = answers[i]

        words = answer.strip().split()
        answer_lower = answer.lower()

        expected = keywords_list[i]

        relevant = any(
            keyword in answer_lower
            for keyword in expected
        )

        if len(words) < 5 or not relevant:

            prediction = "Needs Improvement"

        else:

            try:

                test_data = vectorizer.transform([answer])
                prediction = model.predict(test_data)[0]

                if prediction not in score_map:
                    prediction = "Average"

            except Exception:

                prediction = "Average"

        score = score_map[prediction]
        total_score += score

        results.append({
            "prediction": prediction,
            "score": score
        })

        st.write(f"### Question {i + 1}")
        st.write(questions[i])

        st.write("Evaluation:", prediction)
        st.write(f"Score: {score}/100")

        if prediction == "Good":

            st.success(
                "Good answer! You covered relevant information."
            )

        elif prediction == "Average":

            st.info(
                "Add more details and a practical example."
            )

        else:

            st.warning(
                "Try explaining the concept with relevant details."
            )

        st.divider()

    # OVERALL SCORE

    overall_score = total_score / 3
    # ======================================
    # PERFORMANCE INSIGHTS
    # ======================================

    st.subheader("📊 Performance Insights")

    strengths = []
    improvement_areas = []

    for i in range(3):

        answer_lower = answers[i].lower()
        expected = keywords_list[i]

        covered = [
            word for word in expected
            if word in answer_lower
        ]

        missing = [
            word for word in expected
            if word not in answer_lower
        ]

        if results[i]["prediction"] == "Good":
            strengths.append(
                f"Question {i + 1}: Covered relevant concepts."
            )
        else:
            improvement_areas.append(
                f"Question {i + 1}: Try including "
                + ", ".join(missing[:3])
            )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Strengths")

        if strengths:
            for item in strengths:
                st.success(item)
        else:
            st.info("Keep practising to build your strengths.")

    with col2:
        st.markdown("### 🎯 Areas to Improve")

        if improvement_areas:
            for item in improvement_areas:
                st.warning(item)
        else:
            st.success("Great! No major keyword gaps detected.")

    st.caption(
        "Insights are generated using keyword matching "
        "and the project's local ML evaluation model."
    )

    st.session_state.results = results
    st.session_state.overall_score = overall_score

    # ======================================
    # 10. FINAL INTERVIEW REPORT
    # ======================================

    st.subheader("Final Interview Report")

    st.write(
        "Candidate:",
        st.session_state.candidate_name
    )

    st.write("Job Role:", selected_role)
    st.write("Difficulty:", selected_difficulty)

    st.metric(
        "Overall Score",
        f"{overall_score:.0f}/100"
    )

    st.info(
        "This is an educational ML prototype. "
        "Scores are illustrative and are not a reliable "
        "measure of actual interview performance."
    )

    # ======================================
    # 11. DOWNLOAD PDF
    # ======================================

    pdf_file = generate_pdf_report(
        st.session_state.candidate_name,
        selected_role,
        selected_difficulty,
        questions,
        answers,
        results,
        overall_score
    )

    st.download_button(
        label="Download Interview Report (PDF)",
        data=pdf_file,
        file_name="IntervuAI_Report.pdf",
        mime="application/pdf"
    )

    # ======================================
    # 12. START NEW INTERVIEW
    # ======================================

    if st.button("Start New Interview"):

        st.session_state.interview_started = False
        st.session_state.submitted = False
        st.session_state.current_question = 0

        st.session_state.results = []
        st.session_state.overall_score = 0

        st.rerun()