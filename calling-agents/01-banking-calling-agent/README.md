# Banking Calling Agent — EMI & Payment Reminder

AI voice agent that calls bank customers about due loan EMIs and credit card
payments, verifies identity, records payment intent, reschedules, or transfers
to a human agent. Built with **Vapi** (voice) + **n8n** (orchestration).

## What it does

1. Every day at 10:00 AM, n8n reads the `DueCustomers` Google Sheet.
2. Customers with status `pending` and a due date of today or earlier are
   queued, one by one.
3. Vapi calls each customer with the Banking Payment Reminder assistant
   (Urdu-first voice, `ur-PK-AsadNeural`).
4. The assistant verifies identity (last 4 digits of account/CNIC only),
   states the due amount and date, and offers: pay now, reschedule, or
   speak to a human.
5. When the call ends, Vapi sends an end-of-call report to n8n, which logs
   the outcome in the `CallLog` sheet. If the customer promised to pay,
   a payment link is emailed and the team is notified on Slack.

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
   - `YOUR_GOOGLE_SHEET_ID` — sheet with `DueCustomers` and `CallLog` tabs
   - `YOUR_VAPI_ASSISTANT_ID`, `YOUR_VAPI_PHONE_NUMBER_ID`
   - `YOUR_N8N_URL` — your public n8n URL (webhook base) in the assistant tools
   - `YOUR_PAYMENT_LINK` — your payment gateway link
4. **Sheet columns** (`DueCustomers`): `name`, `phone`, `email`,
   `dueDate` (YYYY-MM-DD), `status` (`pending`/`done`).
5. Set the Vapi assistant's server URL / webhook to your n8n
   `vapi-call-report` webhook so end-of-call reports arrive.

## Safety rules (built into the assistant)

- Never asks for a full card number, PIN, OTP, password, or full CNIC.
- Identity check uses last 4 digits only.
- Angry or complex cases are transferred to a human, never argued with.

## Test it

1. Add one test row to `DueCustomers` with your own number.
2. Run the workflow once in n8n (Execute workflow).
3. Answer the call, say you will pay, hang up — check `CallLog` and Slack.
