# Webhook → Slack Notification Automation

<p>
  <img src="https://img.shields.io/badge/n8n-Workflow-EA4B71?style=flat-square&logo=n8n&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-Powered-412991?style=flat-square&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Category-Alerting-blue?style=flat-square" />
</p>

> Turn any webhook event into an instant, conditional Slack alert.

## ✨ Features

- 🔗 Works with webhooks from any service
- 🎯 Conditional filtering — only important events notify
- 💬 Instant formatted Slack alerts
- ⚡ Lightweight 3-node setup

## 🔄 How it works

```mermaid
flowchart LR
    A[🔗 Webhook Event] --> B{Condition?}
    B -->|Match| C[💬 Slack Alert]
    B -->|No| D[🔇 Ignore]
```

1. A **Webhook node** receives incoming events (test or production URL).
2. An **IF node** filters/conditions which events deserve a notification.
3. Matching events are pushed to **Slack** as a formatted message.

## 🧰 Requirements

| Requirement | Purpose |
|-------------|---------|
| n8n | Workflow automation |
| Slack | Notifications |
| Any webhook source | Event input |

## 🚀 Setup

1. Import `workflow.json` into n8n.
2. Connect your **Slack** credential and choose the target channel.
3. Copy the production webhook URL into the sending service.
4. Send a test event, verify the Slack message, then activate.

## 📁 Files

| File | Description |
|------|-------------|
| `workflow.json` | Ready-to-import n8n workflow (**Workflows → Import from File**) |
| `README.md` | This guide |

> ⚠️ n8n exports never include credentials — reconnect your own after import.
