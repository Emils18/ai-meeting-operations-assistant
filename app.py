import json
import os
from datetime import datetime

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(
    page_title="AI Meeting Operations Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# CUSTOM UI
# -----------------------------
st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(69, 104, 220, 0.16), transparent 32%),
                radial-gradient(circle at top right, rgba(142, 68, 255, 0.12), transparent 28%),
                #080b12;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        [data-testid="stSidebar"] {
            background: rgba(12, 16, 27, 0.96);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        .hero {
            padding: 32px;
            border-radius: 24px;
            background:
                linear-gradient(
                    135deg,
                    rgba(87, 113, 255, 0.18),
                    rgba(130, 66, 255, 0.12)
                );
            border: 1px solid rgba(255, 255, 255, 0.10);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.28);
            margin-bottom: 24px;
        }

        .hero-badge {
            display: inline-block;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(103, 126, 255, 0.15);
            border: 1px solid rgba(137, 153, 255, 0.25);
            color: #bcc7ff;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 14px;
        }

        .hero h1 {
            margin: 0;
            font-size: clamp(34px, 5vw, 58px);
            line-height: 1.05;
            letter-spacing: -2px;
            color: #ffffff;
        }

        .hero p {
            max-width: 800px;
            margin-top: 16px;
            margin-bottom: 0;
            color: #aab3c5;
            font-size: 17px;
            line-height: 1.7;
        }

        .feature-card {
            min-height: 150px;
            padding: 22px;
            border-radius: 20px;
            background: rgba(17, 22, 36, 0.86);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 14px 40px rgba(0, 0, 0, 0.20);
        }

        .feature-icon {
            font-size: 28px;
            margin-bottom: 12px;
        }

        .feature-title {
            color: #ffffff;
            font-size: 16px;
            font-weight: 750;
            margin-bottom: 7px;
        }

        .feature-text {
            color: #8f99ac;
            font-size: 13px;
            line-height: 1.55;
        }

        .section-card {
            padding: 24px;
            border-radius: 22px;
            background: rgba(15, 19, 31, 0.90);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.22);
            margin-bottom: 20px;
        }

        .metric-card {
            padding: 20px;
            border-radius: 18px;
            background: rgba(18, 24, 39, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.08);
            text-align: center;
        }

        .metric-number {
            font-size: 30px;
            font-weight: 800;
            color: #ffffff;
        }

        .metric-label {
            margin-top: 4px;
            font-size: 12px;
            color: #8893a7;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .summary-box {
            padding: 22px;
            border-radius: 18px;
            background: rgba(79, 99, 214, 0.10);
            border: 1px solid rgba(112, 130, 255, 0.18);
            color: #d8def0;
            line-height: 1.75;
        }

        .decision-item,
        .risk-item,
        .sop-item {
            padding: 15px 17px;
            border-radius: 14px;
            margin-bottom: 10px;
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(255, 255, 255, 0.07);
            color: #ced5e4;
            line-height: 1.55;
        }

        .risk-item {
            border-left: 4px solid #ffb84d;
        }

        .decision-item {
            border-left: 4px solid #7187ff;
        }

        .sop-item {
            border-left: 4px solid #46d6a7;
        }

        .footer {
            margin-top: 45px;
            text-align: center;
            color: #626d80;
            font-size: 12px;
        }

        .stButton > button {
            width: 100%;
            min-height: 52px;
            border: 0;
            border-radius: 14px;
            font-weight: 750;
            font-size: 15px;
            background: linear-gradient(135deg, #6577ff, #8d5cff);
            color: white;
            box-shadow: 0 12px 28px rgba(102, 119, 255, 0.28);
            transition: 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 16px 34px rgba(102, 119, 255, 0.38);
        }

        .stDownloadButton > button {
            width: 100%;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(255, 255, 255, 0.04);
            color: #e8ecf5;
        }

        .stTextArea textarea {
            background: rgba(12, 16, 27, 0.88);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 16px;
            color: white;
            min-height: 300px;
        }

        [data-testid="stFileUploaderDropzone"] {
            background: rgba(12, 16, 27, 0.80);
            border: 1px dashed rgba(130, 146, 255, 0.40);
            border-radius: 16px;
        }

        [data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
        }

        div[data-testid="stAlert"] {
            border-radius: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# API FUNCTIONS
# -----------------------------
def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or api_key == "your_actual_api_key_here":
        raise ValueError(
            "Groq API key is missing. Add GROQ_API_KEY inside your .env file."
        )

    return Groq(api_key=api_key)


def analyze_transcript(transcript: str, meeting_type: str) -> dict:
    client = get_groq_client()

    prompt = f"""
You are an AI operations analyst.

Analyze the following {meeting_type.lower()} transcript.

Return valid JSON only using this exact structure:

{{
  "meeting_title": "Professional inferred title",
  "meeting_summary": "Clear professional summary",
  "sentiment": "Positive, Neutral, Mixed, or Urgent",
  "key_decisions": [
    "Decision"
  ],
  "action_items": [
    {{
      "task": "Specific task",
      "owner": "Person responsible or Unassigned",
      "deadline": "Deadline or Not specified",
      "priority": "High, Medium, or Low",
      "status": "Pending"
    }}
  ],
  "sop_steps": [
    "Clear process step"
  ],
  "risks_or_blockers": [
    "Risk, issue, dependency, or blocker"
  ],
  "follow_up_questions": [
    "Question that should be clarified after the meeting"
  ]
}}

Rules:
- Never invent names, deadlines, or decisions.
- Use "Unassigned" when an owner is not mentioned.
- Use "Not specified" when a deadline is missing.
- Keep tasks concise and actionable.
- Return JSON only.
- Do not use markdown fences.

Transcript:
{transcript}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You convert business meeting transcripts into accurate "
                    "structured operational reports."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        max_completion_tokens=3000,
        response_format={"type": "json_object"},
    )

    response_text = completion.choices[0].message.content

    if not response_text:
        raise ValueError("Groq returned an empty response.")

    return json.loads(response_text)


def create_csv(action_items: list[dict]) -> str:
    return pd.DataFrame(action_items).to_csv(index=False)


def create_markdown_report(results: dict) -> str:
    lines = [
        f"# {results.get('meeting_title', 'Meeting Operations Report')}",
        "",
        f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        "",
        "## Executive Summary",
        results.get("meeting_summary", "No summary generated."),
        "",
        "## Key Decisions",
    ]

    decisions = results.get("key_decisions", [])
    lines.extend([f"- {decision}" for decision in decisions] or ["- None identified"])

    lines.extend(["", "## Action Items"])

    action_items = results.get("action_items", [])

    if action_items:
        for item in action_items:
            lines.append(
                f"- **{item.get('task', '')}** — "
                f"Owner: {item.get('owner', 'Unassigned')} | "
                f"Deadline: {item.get('deadline', 'Not specified')} | "
                f"Priority: {item.get('priority', 'Medium')}"
            )
    else:
        lines.append("- None identified")

    lines.extend(["", "## SOP Steps"])

    sop_steps = results.get("sop_steps", [])
    lines.extend(
        [f"{number}. {step}" for number, step in enumerate(sop_steps, 1)]
        or ["No SOP steps identified."]
    )

    lines.extend(["", "## Risks and Blockers"])

    risks = results.get("risks_or_blockers", [])
    lines.extend([f"- {risk}" for risk in risks] or ["- None identified"])

    return "\n".join(lines)


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("## ⚡ Operations Copilot")
    st.caption("AI-powered meeting intelligence")

    st.divider()

    meeting_type = st.selectbox(
        "Meeting type",
        [
            "Operations Meeting",
            "Project Meeting",
            "Client Meeting",
            "Team Meeting",
            "Sales Meeting",
            "Property Management Meeting",
        ],
    )

    st.markdown("### Output includes")

    st.markdown(
        """
        - Executive summary
        - Decisions
        - Action items
        - Owners and deadlines
        - Priority levels
        - SOP recommendations
        - Risks and blockers
        - Follow-up questions
        """
    )

    st.divider()

    st.caption("Model")
    st.code("llama-3.3-70b-versatile", language=None)

    st.caption("API Provider")
    st.code("Groq", language=None)

    st.info(
        "Groq is used as the fast development and testing API provider. "
        "The architecture can be adapted to Claude or OpenAI."
    )


# -----------------------------
# HERO
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">AI OPERATIONS AUTOMATION</div>
        <h1>Turn conversations into execution.</h1>
        <p>
            Upload a meeting transcript and instantly generate a structured
            operations report with summaries, decisions, tasks, deadlines,
            SOP steps, risks, and downloadable outputs.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

feature_columns = st.columns(4)

features = [
    ("🧠", "Smart Summaries", "Convert long discussions into concise executive reports."),
    ("✅", "Action Extraction", "Identify tasks, responsible owners, deadlines, and priority."),
    ("🧭", "SOP Generation", "Transform discussions into repeatable operational processes."),
    ("📤", "Export Ready", "Download structured CSV, JSON, and Markdown reports."),
]

for column, feature in zip(feature_columns, features):
    icon, title, description = feature

    with column:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-text">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")


# -----------------------------
# INPUT AREA
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Meeting input")
st.caption("Upload a TXT transcript or paste the conversation manually.")

uploaded_file = st.file_uploader(
    "Upload transcript",
    type=["txt"],
    label_visibility="collapsed",
)

uploaded_text = ""

if uploaded_file is not None:
    uploaded_text = uploaded_file.read().decode("utf-8", errors="replace")

transcript = st.text_area(
    "Transcript",
    value=uploaded_text,
    placeholder=(
        "Example:\n\n"
        "Sarah: We need to complete the property report by Friday.\n"
        "Michael: I will prepare the occupancy figures by Wednesday..."
    ),
    label_visibility="collapsed",
)

word_count = len(transcript.split()) if transcript else 0
character_count = len(transcript) if transcript else 0

input_info_1, input_info_2, input_info_3 = st.columns(3)

input_info_1.caption(f"Words: **{word_count:,}**")
input_info_2.caption(f"Characters: **{character_count:,}**")
input_info_3.caption(f"Meeting type: **{meeting_type}**")

analyze_button = st.button(
    "⚡ Analyze Meeting",
    type="primary",
    use_container_width=True,
)

st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# ANALYSIS RESULTS
# -----------------------------
if analyze_button:
    if not transcript.strip():
        st.warning("Please upload or paste a meeting transcript first.")
    elif len(transcript.strip()) < 30:
        st.warning("The transcript is too short. Add more meeting content.")
    else:
        try:
            with st.spinner("Analyzing the meeting and building your operations report..."):
                results = analyze_transcript(transcript, meeting_type)

            st.session_state["analysis_results"] = results
            st.success("Meeting analysis completed successfully.")

        except json.JSONDecodeError:
            st.error("The AI returned invalid JSON. Please analyze the transcript again.")

        except Exception as error:
            st.error(f"Analysis failed: {error}")


if "analysis_results" in st.session_state:
    results = st.session_state["analysis_results"]

    action_items = results.get("action_items", [])
    decisions = results.get("key_decisions", [])
    risks = results.get("risks_or_blockers", [])
    sop_steps = results.get("sop_steps", [])

    st.markdown("---")

    st.markdown(
        f"## {results.get('meeting_title', 'Meeting Operations Report')}"
    )

    st.caption(
        f"Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')} "
        f"• Sentiment: {results.get('sentiment', 'Not specified')}"
    )

    metric_columns = st.columns(4)

    metrics = [
        (len(action_items), "Action Items"),
        (len(decisions), "Decisions"),
        (len(sop_steps), "SOP Steps"),
        (len(risks), "Risks"),
    ]

    for column, metric in zip(metric_columns, metrics):
        number, label = metric

        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">{number}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Executive Summary")

    st.markdown(
        f"""
        <div class="summary-box">
            {results.get("meeting_summary", "No summary generated.")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    left_column, right_column = st.columns(2)

    with left_column:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Key Decisions")

        if decisions:
            for decision in decisions:
                st.markdown(
                    f'<div class="decision-item">✓ {decision}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No decisions were identified.")

        st.markdown("</div>", unsafe_allow_html=True)

    with right_column:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Risks and Blockers")

        if risks:
            for risk in risks:
                st.markdown(
                    f'<div class="risk-item">⚠ {risk}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No risks or blockers were identified.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Action Items")

    if action_items:
        action_dataframe = pd.DataFrame(action_items)

        preferred_columns = [
            "task",
            "owner",
            "deadline",
            "priority",
            "status",
        ]

        available_columns = [
            column
            for column in preferred_columns
            if column in action_dataframe.columns
        ]

        action_dataframe = action_dataframe[available_columns]

        action_dataframe.columns = [
            column.replace("_", " ").title()
            for column in action_dataframe.columns
        ]

        st.dataframe(
            action_dataframe,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption("No action items were identified.")

    st.markdown("</div>", unsafe_allow_html=True)

    lower_left, lower_right = st.columns(2)

    with lower_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Suggested SOP")

        if sop_steps:
            for number, step in enumerate(sop_steps, 1):
                st.markdown(
                    f'<div class="sop-item"><strong>{number}.</strong> {step}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No SOP steps were identified.")

        st.markdown("</div>", unsafe_allow_html=True)

    with lower_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Follow-up Questions")

        questions = results.get("follow_up_questions", [])

        if questions:
            for question in questions:
                st.markdown(
                    f'<div class="decision-item">? {question}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No follow-up questions were generated.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Export Report")

    export_1, export_2, export_3 = st.columns(3)

    json_report = json.dumps(results, indent=2)
    markdown_report = create_markdown_report(results)
    csv_report = create_csv(action_items)

    with export_1:
        st.download_button(
            "Download CSV",
            data=csv_report,
            file_name="meeting_action_items.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with export_2:
        st.download_button(
            "Download JSON",
            data=json_report,
            file_name="meeting_operations_report.json",
            mime="application/json",
            use_container_width=True,
        )

    with export_3:
        st.download_button(
            "Download Report",
            data=markdown_report,
            file_name="meeting_operations_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with st.expander("View raw AI response"):
        st.json(results)

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="footer">
        Built with Python, Streamlit, Groq API, and Llama • AI Operations Portfolio Project
    </div>
    """,
    unsafe_allow_html=True,
)