# Education Calling Agent — University Admission Inquiry

AI voice agent that calls students who enquired about admission, explains
programs, checks eligibility, shares fee details, and books a campus visit
or a counselling session. Built with **Vapi** (voice) + **n8n**
(orchestration).

## What it does

1. Every day at 12:00 PM, n8n reads the `Inquiries` Google Sheet.
2. Students with status `new` are queued, one by one.
3. Vapi calls each student with the University Admission Inquiry assistant
   (Urdu-first voice, `ur-PK-AsadNeural`).
4. The assistant asks which program the student wants, checks their last
   qualification and marks for eligibility, shares fee details only from
   the official fee data, and offers a campus visit or a counsellor call.
5. When the call ends, Vapi sends an end-of-call report to n8n, which logs
   the outcome in the `CallLog` sheet. If the student booked a campus
   visit, the visit details are emailed to the student and the team is
   notified on Slack.

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
   - `YOUR_GOOGLE_SHEET_ID` — sheet with `Inquiries` and `CallLog` tabs
   - `YOUR_VAPI_ASSISTANT_ID`, `YOUR_VAPI_PHONE_NUMBER_ID`
   - `YOUR_N8N_URL` — your public n8n URL (webhook base) in the assistant tools
4. **Sheet columns** (`Inquiries`): `name`, `phone`, `email`, `program`,
   `lastQualification`, `status` (`new`/`called`/`done`).
5. Set the Vapi assistant's server URL / webhook to your n8n
   `vapi-call-report` webhook so end-of-call reports arrive.

## Safety rules (built into the assistant)

- Never invents fees, discounts, scholarships, or deadlines — fee details
  come only from the official fee data via the `get_fee_details` tool.
- Never asks for a full CNIC number, bank details, passwords, or any
  payment on the call.
- Eligibility is checked with the `check_eligibility` tool, never guessed.
- Detailed or complex queries are transferred to a human counsellor, and
  the student is never pressured.

## Test it

1. Add one test row to `Inquiries` with your own number.
2. Run the workflow once in n8n (Execute workflow).
3. Answer the call, ask about a program and a campus visit, hang up —
   check `CallLog`, your email, and Slack.
