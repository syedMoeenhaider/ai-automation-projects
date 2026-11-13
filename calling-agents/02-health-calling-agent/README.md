# Health Calling Agent — Clinic Appointment Booking

AI voice agent that calls patients about upcoming clinic appointments — to
confirm the appointment, book a new one, reschedule it, or cancel it. Built
with **Vapi** (voice) + **n8n** (orchestration).

## What it does

1. Every day at 09:00 AM, n8n reads the `Appointments` Google Sheet.
2. Patients with status `pending` and an appointment date within the next
   2 days are queued, one by one.
3. Vapi calls each patient with the Clinic Appointment Booking assistant
   (Urdu-first voice, `ur-PK-AsadNeural`).
4. The assistant confirms the appointment date and time, and offers:
   confirm, reschedule, or cancel. It can also book a new appointment and
   check free slots.
5. When the call ends, Vapi sends an end-of-call report to n8n, which logs
   the outcome in the `CallLog` sheet. If the patient confirmed, a
   confirmation email is sent and the team is notified on Slack.

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
   - `YOUR_GOOGLE_SHEET_ID` — sheet with `Appointments` and `CallLog` tabs
   - `YOUR_VAPI_ASSISTANT_ID`, `YOUR_VAPI_PHONE_NUMBER_ID`
   - `YOUR_N8N_URL` — your public n8n URL (webhook base) in the assistant tools
4. **Sheet columns** (`Appointments`): `name`, `phone`, `email`,
   `appointmentDate` (YYYY-MM-DD), `status` (`pending`/`done`).
5. Set the Vapi assistant's server URL / webhook to your n8n
   `vapi-call-report` webhook so end-of-call reports arrive.

## Safety rules (built into the assistant)

- Never gives medical advice, diagnoses, or treatment suggestions — the
  agent only handles appointment administration.
- Medical questions are passed to the doctor or clinic staff, never answered
  by the agent.
- Never shares other patients' data.

## Test it

1. Add one test row to `Appointments` with your own number and an
   appointment date within the next 2 days.
2. Run the workflow once in n8n (Execute workflow).
3. Answer the call, confirm the appointment, hang up — check `CallLog`,
   your email inbox, and Slack.
