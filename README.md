# AI Meeting Operations Assistant

AI Meeting Operations Assistant is a Python application that converts meeting transcripts into structured operational reports.

The application uses the Groq API to analyze meeting conversations and extract summaries, decisions, action items, deadlines, risks, and recommended standard operating procedures.

## Features

- Upload a meeting transcript as a TXT file
- Paste a transcript manually
- Generate an executive summary
- Extract key decisions
- Identify action items
- Detect task owners and deadlines
- Assign task priority levels
- Generate suggested SOP steps
- Identify risks and blockers
- Generate follow-up questions
- Export action items as CSV
- Export the full result as JSON
- Export a structured Markdown report

## Technologies Used

- Python
- Streamlit
- Groq API
- Llama 3.3
- Pandas
- python-dotenv

## How It Works

1. The user uploads or pastes a meeting transcript.
2. The application sends the transcript to the Groq API.
3. The language model returns structured JSON data.
4. The application validates and displays the results.
5. The user can download the generated reports.

## Project Structure

```text
ai-meeting-operations-assistant/
├── app.py
├── requirements.txt
├── sample_transcript.txt
├── .env.example
├── .gitignore
└── README.md