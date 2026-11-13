# Insurance Calling Agent — Policy Renewal Reminder

AI voice agent that calls policy holders before their renewal date, reminds
them of the premium due, records renewal intent, answers claim-status
questions only from verified data, or transfers to a human agent. Built with
**Vapi** (voice) + **n8n** (orchestration).

## What it does

1. Every day at 10:00 AM, n8n reads the `Policies` Google Sheet.
2. Policy holders with status `pending` and a renewal date within the next
   7 days are queued, one by one.
3. Vapi calls each policy holder with the Insurance Policy Renewal Agent
   (Urdu-first voice, `ur-PK-AsadNeural`).
4. The assistant verifies identity (last 4 digits of the policy number
   only), states the premium due amount and renewal date, and offers:
   renew now, schedule a callback, or speak to a human agent.
5. Claim-status questions are answered only from verified tool data —
   never invented. If no verified data is available, a human agent
   calls back with the real status.
6. When the call ends, Vapi sends an end-of-call report to n8n, which logs
   the outcome in the `CallLog` sheet. If the customer promised to renew,
   a renewal payment link is emailed and the team is notified on Slack.

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
   - `YOUR_GOOGLE_SHEET_ID` — sheet with `Policies` and `CallLog` tabs
   - `YOUR_VAPI_ASSISTANT_ID`, `YOUR_VAPI_PHONE_NUMBER_ID`
   - `YOUR_N8N_URL` — your public n8n URL (webhook base) in the assistant tools
   - `YOUR_RENEWAL_LINK` — your renewal payment link
4. **Sheet columns** (`Policies`): `name`, `phone`, `email`,
   `policyNo`, `premiumDue`, `renewalDate` (YYYY-MM-DD),
   `status` (`pending`/`done`).
5. Set the Vapi assistant's server URL / webhook to your n8n
   `vapi-call-report` webhook so end-of-call reports arrive.

## Safety rules (built into the assistant)

- Never asks for a full policy number, CNIC, bank details, OTP, password,
  or full policy documents.
- Identity check uses last 4 digits of the policy number only.
- Claim outcomes are never invented — only verified tool data is quoted,
  otherwise a human agent calls back.
- Angry or complex cases are transferred to a human, never argued with.

## Test it

1. Add one test row to `Policies` with your own number and a renewal date
   within the next 7 days.
2. Run the workflow once in n8n (Execute workflow).
3. Answer the call, say you will renew, hang up — check `CallLog` and Slack.
