# Contact Form → Google Sheets + Auto Email

Capture contact-form leads in Google Sheets and instantly send a confirmation email.

## ⚙️ How it works

1. An **n8n Form trigger** fires on every submission.
2. **Google Sheets** appends the lead as a new row.
3. **Gmail** immediately sends a confirmation/auto-reply to the submitter.

## 🔑 Requirements

- n8n
- Google Sheets credential
- Gmail credential

## 🧩 Setup

1. Import `workflow.json` into n8n.
2. Create a Google Sheet and connect the **Google Sheets** credential; map the columns.
3. Connect your **Gmail** credential and customize the reply subject/body.
4. Test with the form URL, then activate.

## 📁 Files

- `workflow.json` — ready-to-import n8n workflow (**Workflows → Import from File**)
- `README.md` — this guide

> ⚠️ Credentials are never exported — reconnect your own after import.
