# AI Meeting Operations Assistant

AI Meeting Operations Assistant is a Python application that transforms meeting transcripts into structured operational reports using the Groq API and Llama 3.3.

The application extracts actionable business information including executive summaries, decisions, action items, owners, deadlines, risks, SOP recommendations, and follow-up questions.

---

## Features

- Upload TXT meeting transcripts
- Manual transcript input
- Executive summary generation
- Decision extraction
- Action item tracking
- Owner and deadline identification
- Priority classification
- SOP generation
- Risk and blocker detection
- Follow-up question generation
- CSV export
- JSON export
- Markdown report export

---

## Screenshots

### Dashboard

![Dashboard](assets/dashboard.png)

The landing page provides a clean operational dashboard where users can configure meeting types, review supported outputs, and submit transcripts for analysis.

---

### Transcript Analysis

![Transcript Analysis](assets/analysis.png)

Users can upload or paste meeting transcripts and process them using the Groq API. The application validates the input before generating structured operational data.

---

### Generated Report

![Generated Report](assets/report-overview.png)

After analysis, the application generates:

- Executive Summary
- Key Decisions
- Risks and Blockers
- Action Metrics

---

### Action Management

![Action Items](assets/action-items.png)

Structured task extraction includes:

- Task description
- Assigned owner
- Deadline
- Priority
- Status

---

### SOP and Follow-up Generation

![SOP](assets/sop.png)

The assistant generates suggested Standard Operating Procedures together with unanswered questions that require clarification during future meetings.

---

### Export Options

![Exports](assets/export.png)

Reports can be exported as:

- CSV
- JSON
- Markdown Report

---

## Technology Stack

- Python
- Streamlit
- Groq API
- Llama 3.3 70B
- Pandas
- python-dotenv

---

## Installation

...
