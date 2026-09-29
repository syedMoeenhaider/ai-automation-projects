# AI Student Acknowledgement + Status Tracking

Scheduled AI-generated acknowledgement emails for students, with status tracking in Google Sheets.

## ⚙️ How it works

1. A **Schedule trigger** runs the workflow periodically.
2. **Google Sheets** rows are read and filtered with an **IF node** (e.g. pending acknowledgements).
3. An **LLM Chain** (OpenAI) drafts a personalized acknowledgement message per student.
4. **Gmail** sends the message; the sheet row is then **updated** with the sent status.

## 🔑 Requirements

- n8n
- OpenAI API credential
- Google Sheets credential
- Gmail credential

## 🧩 Setup

1. Import `workflow.json` into n8n.
2. Point the Google Sheets nodes at your student spreadsheet and reconnect credentials.
3. Reconnect the **OpenAI** chat model inside the LLM Chain.
4. Run once manually to verify emails + status updates, then activate the schedule.

## 📁 Files

- `workflow.json` — ready-to-import n8n workflow (**Workflows → Import from File**)
- `README.md` — this guide

> ⚠️ Credentials are never exported — reconnect your own after import.
