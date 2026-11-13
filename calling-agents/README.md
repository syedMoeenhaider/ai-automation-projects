# 8 AI Calling Agent Projects

Eight production-style voice calling agents, each built with **Vapi**
(voice AI) + **n8n** (orchestration). Every project has an n8n workflow,
a Vapi assistant config, a README, and a rendered workflow diagram.

## The 8 projects

| # | Project | What the agent does |
|---|---|---|
| 01 | Banking Calling Agent | EMI / credit card payment reminders, identity check, payment intent, reschedule, human transfer |
| 02 | Health Calling Agent | Clinic appointment booking, reminders, reschedule/cancel |
| 03 | E-commerce Calling Agent | Order confirmation, COD verification, delivery updates |
| 04 | Real Estate Calling Agent | Property inquiry handling, site-visit booking |
| 05 | Restaurant Calling Agent | Food order confirmation, address check, delivery ETA |
| 06 | Education Calling Agent | University admission inquiry, eligibility check, campus visit booking |
| 07 | Travel Calling Agent | Hotel / flight booking confirmation, itinerary changes |
| 08 | Insurance Calling Agent | Policy renewal reminders, premium due, claim status |

## Stack (same for all 8)

- **Voice:** Vapi — `gpt-4o-mini`, Deepgram `nova-3` transcription,
  Azure `ur-PK-AsadNeural` voice (Urdu-first, switches to English)
- **Orchestration:** n8n — schedule / sheets / HTTP calls to Vapi /
  end-of-call report webhook / logging / notifications
- **Data:** Google Sheets (customer list + call log) — swap for any CRM

## How to use any project

1. Open the project folder, read its README.
2. Create the Vapi assistant from `vapi-assistant.json`.
3. Import `workflow.json` in n8n, connect your credentials, replace the
   `YOUR_...` placeholders (sheet ID, assistant ID, phone number ID,
   n8n URL).
4. Add one test row with your own number and run it once.

## Placeholders

Every file uses `YOUR_...` placeholders for secrets and IDs. Nothing here
contains a real API key, phone number, or customer data.
