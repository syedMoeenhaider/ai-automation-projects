# Instagram Keyword Search + Data Collection

Scrape Instagram posts by keyword with Apify and collect the dataset for research or outreach.

## ⚙️ How it works

1. Keywords are read from a **Google Sheet**.
2. The **Apify Instagram Keyword Search Scraper** actor runs per keyword (up to 6 posts each).
3. Dataset items are retrieved and ready for downstream processing or export.

## 🔑 Requirements

- n8n
- Apify account + credential
- Google Sheets credential

## 🧩 Setup

1. Import `workflow.json` into n8n.
2. Connect your **Apify** credential and add keywords to the source Google Sheet (column `Search keyword`).
3. Run manually once to verify the actor output, then schedule or trigger as needed.

## 📁 Files

- `workflow.json` — ready-to-import n8n workflow (**Workflows → Import from File**)
- `README.md` — this guide

> ⚠️ Credentials are never exported — reconnect your own after import.
