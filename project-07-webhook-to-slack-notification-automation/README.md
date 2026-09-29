# Webhook → Slack Notification Automation

Turn any webhook event into an instant, conditional Slack alert.

## ⚙️ How it works

1. A **Webhook node** receives incoming events (test or production URL).
2. An **IF node** filters/conditions which events deserve a notification.
3. Matching events are pushed to **Slack** as a formatted message.

## 🔑 Requirements

- n8n
- Slack credential

## 🧩 Setup

1. Import `workflow.json` into n8n.
2. Connect your **Slack** credential and choose the target channel.
3. Copy the production webhook URL into the sending service.
4. Send a test event, verify the Slack message, then activate.

## 📁 Files

- `workflow.json` — ready-to-import n8n workflow (**Workflows → Import from File**)
- `README.md` — this guide

> ⚠️ Credentials are never exported — reconnect your own after import.
