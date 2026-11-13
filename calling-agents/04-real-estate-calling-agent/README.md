# Real Estate Calling Agent — Property Inquiry & Site-Visit Booking

AI voice agent that calls new property leads, understands their budget,
area, and property type, answers basic questions, and books a site visit
with a real estate agent. Built with **Vapi** (voice) + **n8n**
(orchestration).

## What it does

1. Every day at 11:00 AM, n8n reads the `Leads` Google Sheet.
2. Leads with status `new` are queued, one by one.
3. Vapi calls each lead with the Real Estate Site-Visit Booking Agent
   (Urdu-first voice, `ur-PK-AsadNeural`).
4. The assistant asks for budget range, preferred area, property type
   (house / flat / plot), and bedrooms, suggests matching property types,
   and offers a site visit on a day and time the lead chooses. It never
   quotes a fake exact price — the agent confirms pricing on the visit.
5. When the call ends, Vapi sends an end-of-call report to n8n, which logs
   the outcome in the `CallLog` sheet. If a visit was booked, the visit
   details are emailed to the lead and the team is notified on Slack.

## Files

| File | What it is |
|---|---|
| `workflow.json` | n8n workflow — import it in n8n (13 nodes) |
| `vapi-assistant.json` | Vapi assistant config — create it via the Vapi dashboard or API |
| `workflow.png` | Rendered workflow diagram |

## Setup

1. **Vapi**: create a phone number in Vapi, then create the assistant from
   `vapi-assistant.json` (dashboard → Assistants → Import, or
   `POST https://api.vapi.ai/assistant`). Copy the assistant ID and phone
   number ID into the n8n workflow.
2. **n8n**: import `workflow.json`. Connect your own credentials:
   Google Sheets, Vapi API key (HTTP Header Auth), Gmail, Slack.
3. Replace the placeholders:
   - `YOUR_GOOGLE_SHEET_ID` — sheet with `Leads` and `CallLog` tabs
   - `YOUR_VAPI_ASSISTANT_ID`, `YOUR_VAPI_PHONE_NUMBER_ID`
   - `YOUR_N8N_URL` — your public n8n URL (webhook base) in the assistant tools
4. **Sheet columns** (`Leads`): `name`, `phone`, `email`, `budget`,
   `area`, `propertyType` (`house`/`flat`/`plot`), `status` (`new`/`done`).
5. Set the Vapi assistant's server URL / webhook to your n8n
   `vapi-call-report` webhook so end-of-call reports arrive.

## Safety rules (built into the assistant)

- Never quotes a fake exact price — pricing is confirmed by the agent.
- Price negotiation and payment plans go to a human agent, never the bot.
- Not-interested leads are thanked politely and never pressured.

## Test it

1. Add one test row to `Leads` with your own number.
2. Run the workflow once in n8n (Execute workflow).
3. Answer the call, give a budget and area, book a visit — check `CallLog`,
   your email, and Slack.
