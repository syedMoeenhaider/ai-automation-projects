# 🤖 AI Automation Projects

A curated collection of **AI-powered automation workflows** built with [n8n](https://n8n.io) — ready to import, customize, and deploy.

Each project lives in its own folder with a ready-to-import `workflow.json` and a dedicated `README.md` explaining what it does, how it works, and how to set it up.

## 📦 Projects

| # | Project | What it does |
|---|---------|--------------|
| 01 | [Form Validation + AI Tag Generator](project-01-form-validation-ai-tag-generator/) | Validate form submissions & auto-generate smart AI tags |
| 02 | [Contact Form → Google Sheets + Auto Email](project-02-contact-form-to-google-sheets-and-auto-email/) | Capture leads in Sheets & send instant confirmation emails |
| 03 | [QuickMart API → Supabase + Data Analysis](project-03-quickmart-api-to-supabase-and-data-analysis/) | Daily ingestion, snapshot history, analysis & reporting |
| 04 | [LinkedIn AI Content Pipeline](project-04-linkedin-ai-content-pipeline/) | AI trend research → writing → human approval → auto-publish |
| 05 | [Instagram Keyword Search + Data Collection](project-05-instagram-keyword-search-and-data-collection/) | Scrape Instagram posts by keyword via Apify |
| 06 | [TikTok → Facebook Automation (Apify)](project-06-tiktok-to-facebook-automation-with-apify/) | Scrape TikTok & republish to Facebook via Graph API |
| 07 | [Webhook → Slack Notifications](project-07-webhook-to-slack-notification-automation/) | Real-time conditional Slack alerts from webhooks |
| 08 | [TikTok → Facebook Page Automation](project-08-tiktok-to-facebook-page-automation/) | Scheduled discovery, dedupe & auto-posting with AI captions |
| 09 | [AI Lead Qualification](project-09-ai-lead-qualification-automation/) | Score leads HOT/WARM/COLD with GPT & auto-respond |
| 10 | [AI Student Acknowledgement + Tracking](project-10-ai-student-acknowledgement-and-status-tracking/) | AI acknowledgement emails with Sheets status tracking |

## 🚀 How to use

1. Pick a project folder and read its `README.md`.
2. In n8n, go to **Workflows → Import from File** and select the project's `workflow.json`.
3. Reconnect credentials (OpenAI, Gmail, Google Sheets, Slack, Supabase, Apify…) as listed in the project README.
4. Follow the setup steps, run a test, then **activate** the workflow.

> ⚠️ Exported workflows don't include credentials — you'll always reconnect your own after import.

## 🛠️ Tech stack

- **n8n** — workflow automation
- **OpenAI (GPT)** — classification, tagging, captions & content generation
- **Supabase** — Postgres database for snapshots
- **Google Sheets / Gmail** — logging & notifications
- **Slack** — team alerts
- **Apify / RapidAPI** — social-media scraping
- **Facebook Graph API / LinkedIn API** — auto-publishing

## 👤 Author

**Syed Moeen Haider** — AI Automation Engineer
